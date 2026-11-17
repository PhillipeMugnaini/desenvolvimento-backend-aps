
from pydantic import BaseModel, EmailStr, Field


class LoginEntrada(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1)


class TokenSaida(BaseModel):
    access_token: str
    token_type: str = "bearer"
