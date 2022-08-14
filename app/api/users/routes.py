from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from app.db.db import get_db
from .schemas import UserResponse, UserRequest
from db.models import User
from utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from db.db import Session
from ..common_schemas import TokenSchema
from ..deps import get_current_user

router = APIRouter(
    prefix="/users"
)

@router.post('/signup', response_model=UserResponse)
async def create_user(data: UserRequest, session: Session = Depends(get_db)):
    try:
        if session.query(User).filter_by(username= data.username).first():
            raise HTTPException(status.HTTP_409_CONFLICT, "Username is already in use")
    
        if session.query(User).filter_by(email= data.email).first():
            raise HTTPException(status.HTTP_409_CONFLICT, "Email is already in use")

        user = User (
                username = data.username,
                email = data.email,
                password = get_hashed_password(data.password),
            )
        session.add(user)
        session.commit()
        return UserResponse(id= user.id, username= user.username, email= user.email)
        
    except AssertionError as exception_message:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, exception_message.__str__())

@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    print(form_data.username)
    user = session.query(User).filter_by(username= form_data.username).first()
    
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

@router.get("/me")
async def read_users_me(current_user: UserResponse = Depends(get_current_user), session: Session = Depends(get_db), response_model= UserResponse):
    user = session.query(User).filter_by(email= current_user.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},)
            
    return UserResponse(id= user.id, email= user.email, username= user.username,)

@router.get('/')
def get_users(session: Session = Depends(get_db)):
    users = session.query(User).all()
    response_users = []
    if not users:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No Users")
    for user in users:
        response_users.append(user.to_response())
    
    return response_users
