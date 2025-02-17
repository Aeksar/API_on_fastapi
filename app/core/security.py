from fastapi import Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Annotated, Union
import jwt

from app.db.models import User
from app.db.database import get_async_session
from app.core.config import settings
from app.utils.rep_utils import sqlalchemy_to_pydantic

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")
pwd_context = CryptContext(schemes=["bcrypt"])

def verify_password(inp_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(inp_password, hashed_password)


def get_hashed_password(password: str):
    return pwd_context.hash(password)


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    query = await session.execute(select(User).where(User.username == username))
    user = query.scalars().first()
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    query = await session.execute(select(User).where(User.email == email))
    user = query.scalars().first()
    return user


async def authenticate(session: AsyncSession, username: str, password: str) -> User:
    user = await get_user_by_username(session, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check your password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_token(data: dict, exp: timedelta | None=None):
    to_encode = data.copy()
    if exp:
        expire = datetime.now() + exp
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_token_from_cookie_or_header(
    request: Request,
    token_from_header: str = Depends(oauth2_scheme)
) -> Union[str, None]:
    token_from_cookie = request.cookies.get('access_token')
    if token_from_cookie:
        return token_from_cookie
    return token_from_header


async def get_current_user(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    token: Annotated[Union[str, None], Depends(get_token_from_cookie_or_header)]
    ):
    credentails_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate data",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentails_exception
    
    try:
        payload: dict = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentails_exception
    except jwt.InvalidTokenError:
        raise credentails_exception
    user = await get_user_by_username(session, username=username)
    if user is None:
        raise credentails_exception
    return sqlalchemy_to_pydantic(user)



