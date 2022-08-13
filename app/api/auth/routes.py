from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from uuid import uuid4, UUID
from jose import jwt, JWTError
from .schemas import UserResponse, UserRequest, TokenData
from db.models import User
from utils import get_hashed_password, verify_password, create_access_token, create_refresh_token, JWT_SECRET_KEY, ALGORITHM
from db.db import Session
from ..common_schemas import TokenSchema

router = APIRouter(
    prefix="/auth"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

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
    
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email= email)
        except JWTError:
            raise credentials_exception
        user = s.query(User).filter_by(email=token_data.email).first()
        if user is None:
            raise credentials_exception
        return user
    
    @router.get("/users/me")
    async def read_users_me(current_user: UserResponse = Depends(get_current_user), response_model= UserResponse):
        return UserResponse(id= current_user.id, email= current_user.email, username= current_user.username,)
    
    @router.get('/users')
    def get_users():
        users = s.query(User).all()
        response_users = []
        if not users:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No Users")
        for user in users:
            response_users.append(user.to_response())
        
        return response_users
