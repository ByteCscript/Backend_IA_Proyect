# app/schemas/users.py

from typing import List, Optional
from pydantic import BaseModel, EmailStr

class RoleOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    roles: List[int] = []   # IDs de rol

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    hashed_password: str           # <-- añadido
    roles: List[RoleOut]

    class Config:
        orm_mode = True
