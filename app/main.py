from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router

app = FastAPI(title="Trimly", description="A production-grade URL shortener")

app.include_router(router)

# Attach a file server to my app at /static, serve files from static
# folder, then call it static
app.mount("/", StaticFiles(directory="static", html=True), name="static")