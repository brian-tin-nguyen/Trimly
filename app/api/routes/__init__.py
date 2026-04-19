import random
import string
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import redis
from app.db.session import AsyncSessionLocal
from app.models import Click, Url
from app.schemas import ShortenRequest, ShortenResponse

router = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))


@router.post("/api/shorten", response_model=ShortenResponse, status_code=201)
async def shorten_url(request: ShortenRequest, db: AsyncSession = Depends(get_db)):
    short_code = generate_short_code()
    original_url = str(request.url)

    url = Url(short_code=short_code, original_url=original_url)
    db.add(url)
    await db.commit()
    await db.refresh(url)

    await redis.set(f"url:{short_code}", original_url, ex=86400)

    return ShortenResponse(
        short_code=short_code,
        short_url=f"http://localhost:8000/{short_code}",
        original_url=original_url,
    )


@router.get("/{short_code}")
async def redirect_url(short_code: str, request: Request, db: AsyncSession = Depends(get_db)):
    original_url = await redis.get(f"url:{short_code}")

    if original_url:
        click = Click(
            short_code=short_code,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
        )
        db.add(click)
        await db.commit()
        return RedirectResponse(url=original_url, status_code=302)

    result = await db.execute(select(Url).where(Url.short_code == short_code, Url.is_active == True))
    url = result.scalar_one_or_none()

    if not url:
        raise HTTPException(status_code=404, detail="Short link not found")

    await redis.set(f"url:{short_code}", url.original_url, ex=86400)

    click = Click(
        short_code=short_code,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(click)
    await db.commit()

    return RedirectResponse(url=url.original_url, status_code=302)