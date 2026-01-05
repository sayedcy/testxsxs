from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models import ScanStatus

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str  # NO VALIDATION - accepts any password of any length

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class ScanJobCreate(BaseModel):
    domain: str

class ScanJobResponse(BaseModel):
    id: int
    domain: str
    status: ScanStatus
    owner_id: int
    created_at: datetime
    updated_at: datetime
    current_step: Optional[str] = None
    progress: int = 0
    subfinder_results: Optional[str] = None
    httpx_results: Optional[str] = None
    nuclei_results: Optional[str] = None
    katana_results: Optional[str] = None
    xss_results: Optional[str] = None
    dalfox_results: Optional[str] = None
    
    model_config = {"from_attributes": True}

