from pydantic import BaseModel, validator, EmailStr


class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr

