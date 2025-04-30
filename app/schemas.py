from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import re

class POIImageBase(BaseModel):
    image_data: str
    is_primary: bool = False

class POIImageCreate(POIImageBase):
    pass

class POIImage(POIImageBase):
    id: int
    poi_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class POIBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    submitted_by: Optional[str] = Field(None, max_length=255)
    
    @validator('latitude')
    def validate_latitude(cls, v):
        if v < -90 or v > 90:
            raise ValueError('Latitude must be between -90 and 90 degrees')
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        if v < -180 or v > 180:
            raise ValueError('Longitude must be between -180 and 180 degrees')
        return v

class POICreate(POIBase):
    pass

class POICreateWithImage(POIBase):
    images: List[Optional[str]]= None

class POIUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    address: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=100)

class POI(POIBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_approved: bool
    is_rejected: bool
    rejection_reason: Optional[str] = None
    moderation_date: Optional[datetime] = None
    images: List[POIImage] = []
    
    class Config:
        orm_mode = True

class POIApprove(BaseModel):
    token: str 
    
    @validator('token')
    def validate_name(cls, v):
        if len(v) < 1 or len(v) > 255:
            raise ValueError('API token is invalid')
        return v
    
class POIReject(BaseModel):
    token: str
    reason: str = Field(..., min_length=1, max_length=255)
    
    @validator('token')
    def validate_name(cls, v):
        if len(v) < 1 or len(v) > 255:
            raise ValueError('API token is invalid')
        return v
    @validator('reason')
    def validate_reason(cls, v):
        if len(v) < 1 or len(v) > 255:
            raise ValueError('Rejection reason must be between 1 and 255 characters')
        return v

class APIKey(BaseModel):
    key: str
    
    class Config:
        orm_mode = True
        
class APIKeyCreate(BaseModel):
    key: str
    name: str
    
    @validator('key')
    def validate_key(cls, v):
        if not re.match(r'^[A-Za-z0-9-_=]+$', v):
            raise ValueError('Invalid API key format')
        return v
    @validator('name')
    def validate_name(cls, v):
        if len(v) < 1 or len(v) > 255:
            raise ValueError('API key name must be between 1 and 255 characters')
        return v