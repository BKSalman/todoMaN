from pydantic import BaseModel
from uuid import UUID

class UserResponse(BaseModel):
     id: UUID
     username: str
     email: str
    

class UserRequest(BaseModel):
     username: str
     email: str
     password: str

class TokenData(BaseModel):
    email: str | None = None
