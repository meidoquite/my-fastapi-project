from pydantic import BaseModel, HttpUrl
from datetime import datetime

class ShortURLBase(BaseModel):
    original_url: str

class ShortURLCreate(ShortURLBase):
    pass

class ShortURLInfo(BaseModel):
    id: int
    original_url: str
    short_key: str
    created_at: datetime
    clicks: int
    short_url: str
    
    class Config:
        from_attributes = True