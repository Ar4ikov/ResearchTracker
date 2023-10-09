from sqlmodel import create_engine, Session
from os import environ
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Annotated

from src.backend.database import User
from src.backend.intertnal import TokenData

# case with postgresql, mysql, sqlite
engine = {
    environ.get('DATABASE_URL').startswith("postgresql"): create_engine(environ.get('DATABASE_URL')),
    environ.get('DATABASE_URL').startswith("mysql"): create_engine(environ.get('DATABASE_URL')),
    environ.get('DATABASE_URL').startswith("sqlite"): create_engine(
        environ.get('DATABASE_URL'), connect_args={"check_same_thread": False}
    ),
}[True]

SECRET_KEY = 'aa6651f1b13dc62b614162e43cb37a6de2b451d64310d75fe66ff0f025105149'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/login')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    with Session(engine) as session:
        user = User.get_by_username(session, username=username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, username=username)
    except JWTError:
        raise credentials_exception
    with Session(engine) as session:
        user = User.get_by_username(session, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
