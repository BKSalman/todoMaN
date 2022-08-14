from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from fastapi import HTTPException
import re
from api.users.schemas import UserResponse

Base = declarative_base()

class Item(Base):
     __tablename__ = "items"

     id = Column(Integer, primary_key=True)
     name = Column(String)

     def __repr__(self):
         return f"Item(id={self.id!r}, name={self.name!r})"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    @validates("username")
    def validate_username(self, key, username):
        print(key)
        if not username:
             raise AssertionError("no Username was provided")
        
        if len(username) < 5 or len(username) > 20:
            raise AssertionError("Username must be between 5 and 20 characters") 
        
        return username 
    
    @validates("email")
    def validate_email(self, key, email):
        print(key)
        if not email:
             raise AssertionError("no Email was provided")
        
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError("Provided email is not an email address") 
        
        return email
     
    def to_response(self) -> UserResponse:
        return UserResponse(id= self.id, username= self.username, email= self.email)
    
    def __repr__(self):
       return f"User(id={self.id!r}, username={self.username!r})"