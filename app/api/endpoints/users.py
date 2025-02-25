from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from typing import Annotated

from app.db.database import get_async_session
from app.db.models import User
from app.api.schemas.user import UserFullSchema, UserBaseSchema, UserUpdate
from app.repositories.user_repository import SQLAlchemyUserRepository
from app.core.config import settings
from app.core.security import (
    get_current_user,
    authenticate,
    create_token,
    get_user_by_username,
    get_user_by_email, 
    get_hashed_password
)


user_router = APIRouter(prefix="/user")

async def get_user_rep(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return SQLAlchemyUserRepository(session)

@user_router.post(
    '/create',
    response_model=UserFullSchema,
    status_code=status.HTTP_201_CREATED)
async def create_user(
    rep: Annotated[SQLAlchemyUserRepository, Depends(get_user_rep)],
    userC: UserBaseSchema
    ):
    return await rep.create_user(userC)

@user_router.get("/all", response_model=list[UserFullSchema])
async def show_all_users(rep: Annotated[SQLAlchemyUserRepository, Depends(get_user_rep)]):
    return await rep.get_users()

@user_router.get("/{user_id}")
async def show_one_user(
    rep: Annotated[SQLAlchemyUserRepository, Depends(get_user_rep)],
    user_id: int
    ):
    return await rep.get_user(user_id)

@user_router.put("/update/{user_id}")
async def update_user(
    rep: Annotated[SQLAlchemyUserRepository, Depends(get_user_rep)],
    user_id: int,
    owner: Annotated[UserFullSchema, Depends(get_current_user)],
    modelUpdate: UserUpdate,
):
    user = await rep.get_user(user_id)
    if owner.role != "admin" or user.username != owner.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No rights for this action"
        )
    
    return await rep.update_user(user_id, modelUpdate)

@user_router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    owner: Annotated[UserFullSchema, Depends(get_current_user)],
    rep: Annotated[SQLAlchemyUserRepository, Depends(get_user_rep)],
    user_id: int,
):
    if owner.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No rights for this action"
        )
    delete = await rep.delete_user(user_id)
    if delete:
        return

@user_router.get("/tasks/{user_id}")
async def user_tasks(
    rep: Annotated[SQLAlchemyUserRepository, Depends(get_user_rep)],
    user_id: int,
):
    return await rep.user_task(user_id)

@user_router.post('/token')
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    response: Response
) -> JSONResponse:
    user = await authenticate(session, form_data.username, form_data.password)
    exp = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_token = create_token(data={"sub": user.username}, exp=exp)
    response = JSONResponse(content={
          "access_token": jwt_token,
          "token_type": "Bearer",

      })
    response.headers["Authorization"] = f"Bearer {jwt_token}"
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return response

@user_router.post(
    "/registration",
    response_model=UserFullSchema,
    status_code=status.HTTP_201_CREATED)
async def reg_user(
    form_data: UserBaseSchema, 
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    check_username = await get_user_by_username(session, form_data.username)
    if check_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username registration yet"
        )
    check_email = await get_user_by_email(session, form_data.username)
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email registration yet"
        )
    new_user = form_data
    new_user.password = get_hashed_password(form_data.password)
    rep = SQLAlchemyUserRepository(session=session)
    return await rep.create_user(form_data)


@user_router.get("/me/task")
async def user_tasks(
    owner: Annotated[UserFullSchema, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
    ):
    rep = SQLAlchemyUserRepository(session=session)
    user = await get_user_by_username(session, owner.username)
    tasks = await rep.user_task(user.id)
    return {"owner_task": tasks}