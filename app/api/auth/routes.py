from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from uuid import uuid4, UUID
from .schemas import UserResponse, UserRequest
from db.models import User
from utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from db.db import Session
from ..common_schemas import TokenSchema
from ..deps import get_current_user

router = APIRouter(
    prefix="/auth"
)

with Session() as s :
    @router.post('/signup', response_model=UserResponse)
    async def create_user(data: UserRequest):
        try:
            if s.query(User).filter_by(username= data.username).first():
                raise HTTPException(status.HTTP_409_CONFLICT, "Username is already in use")
        
            if s.query(User).filter_by(email= data.email).first():
                raise HTTPException(status.HTTP_409_CONFLICT, "Email is already in use")
            user = User (
                    username = data.username,
                    email = data.email,
                    password = get_hashed_password(data.password),
                )
            s.add(user)
            s.commit()
            return UserResponse(id= user.id, username= user.username, email= user.email)
            
        except AssertionError as exception_message:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, exception_message.__str__())
    
    @router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
    async def login(form_data: OAuth2PasswordRequestForm = Depends()):
        print(form_data.username)
        user = s.query(User).filter_by(username= form_data.username).first()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username"
            )
        
        hashed_pass = user.password
        if not verify_password(form_data.password, hashed_pass):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password"
            )
    
        return TokenSchema(
            access_token= create_access_token(user.email),
            refresh_token= create_refresh_token(user.email),
        )
    
        # user = s.query(User).filter_by(email=token_data.email).first()
        # if user is None:
        #     raise credentials_exception
        # return user
    
    @router.get("/users/me")
    async def read_users_me(current_user: UserResponse = Depends(get_current_user), response_model= UserResponse):
        user = s.query(User).filter_by(email= current_user.email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},)
                
        return UserResponse(id= user.id, email= user.email, username= user.username,)
    
    @router.get('/users')
    def get_users():
        users = s.query(User).all()
        response_users = []
        if not users:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No Users")
        for user in users:
            response_users.append(user.to_response())
        
        return response_users
