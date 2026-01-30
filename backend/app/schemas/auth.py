from pydantic import BaseModel, EmailStr, Field, ConfigDict


class EmployeeBase(BaseModel):
    email: EmailStr


class EmployeeCreate(EmployeeBase):
    password: str = Field(..., min_length=6, max_length=128)
    is_admin: bool = False


class EmployeeRead(EmployeeBase):
    id: int
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: EmailStr | None = None


class LoginRequest(BaseModel):
    username: EmailStr
    password: str
