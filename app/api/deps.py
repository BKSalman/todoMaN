from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .auth.schemas import TokenData
from utils import JWT_SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

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
    return token_data
