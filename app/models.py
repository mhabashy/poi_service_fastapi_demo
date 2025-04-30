from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class POI(Base):
    __tablename__ = "pois"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(255))
    category = Column(String(100))
    submitted_by = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    is_approved = Column(Boolean, default=False)
    is_rejected = Column(Boolean, default=False)
    rejection_reason = Column(Text)
    moderation_date = Column(DateTime(timezone=True))
    
    images = relationship("POIImage", back_populates="poi")

class POIImage(Base):
    __tablename__ = "poi_images"
    
    id = Column(Integer, primary_key=True, index=True)
    poi_id = Column(Integer, ForeignKey("pois.id", ondelete="CASCADE"), nullable=False)
    image_data = Column(Text, nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    poi = relationship("POI", back_populates="images")

class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())