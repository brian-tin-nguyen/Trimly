# generates random ID #s
import uuid

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func

from app.db.session import Base

# Stores shortended links, creates short link, one row gets added here
class Url(Base):
    __tablename__ = "urls"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # generates rando ID no two URLs has same
    short_code = mapped_column(String(10), unique=True, nullable=False, index=True) # the (abc123) of short link, UNIQUE
    original_url = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now()) # timestamp
    is_active = mapped_column(Boolean, default=True, nullable=False) # Is this link active 

    clicks = relationship("Click", back_populates="url") # shortcuts that lets us write url.clicks to get click records

# Stores every single click event, every visit gets one row added
class Click(Base):
    __tablename__ = "clicks"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    short_code = mapped_column(String(10), ForeignKey("urls.short_code"), nullable=False)
    clicked_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    ip_address = mapped_column(String(45), nullable=True)
    user_agent = mapped_column(Text, nullable=True)

    url = relationship("Url", back_populates="clicks")