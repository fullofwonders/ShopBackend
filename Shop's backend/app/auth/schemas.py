from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str = Field(description="Email")
    password: str = Field(min_length=6, description="Password")

class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"