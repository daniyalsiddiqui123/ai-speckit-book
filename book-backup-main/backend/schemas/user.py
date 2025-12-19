from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: UUID
    email: str

    class Config:
        from_attributes = True
