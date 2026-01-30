from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.core.security import get_password_hash


class EmployeeCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    is_admin: bool = False

    def get_hashed_password(self):
        return get_password_hash(self.password)


class EmployeeOut(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
