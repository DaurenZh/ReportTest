from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from models import UserRole


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72, description="Password (6-72 characters, bcrypt limitation)")
    role: Optional[UserRole] = UserRole.staff


class UserLogin(BaseModel):
    username: str
    password: str = Field(..., max_length=72)


class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Report schemas
class ReportBase(BaseModel):
    category: str
    message: str = Field(..., min_length=1)


class ReportCreate(ReportBase):
    pass


class ReportResponse(ReportBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
