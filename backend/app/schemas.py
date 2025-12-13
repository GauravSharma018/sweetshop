from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int


class SweetResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    quantity: int

    class Config:
        orm_mode = True
