from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    key: str
    email: EmailStr
    hashed_password: str

class User(BaseModel):
    key: str
    email: EmailStr

class UserUpdate(BaseModel):
    password: str