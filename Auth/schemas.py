from pydantic import BaseModel, EmailStr, Field

class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=6)


class User(BaseModel):
    username: str
    token: str


class UserOut(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool

class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'