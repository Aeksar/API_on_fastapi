from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.database import get_async_session
from app.api.schemas.user import UserSchema, UserCreate, UserUpdate
from app.repositories.user_repository import SQLAlchemyUserRepository


user_router = APIRouter(prefix="/user")

async def get_user_rep(session: Annotated[AsyncSession, Depends(get_async_session)]) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session=session)

@user_router.post(
    '/registr',
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED)
async def create_user(
    rep: Annotated[SQLAlchemyUserRepository, Depends(get_user_rep, use_cache=False)],
    userC: UserCreate
    ):
    return await rep.create_user(userC)

@user_router.get("/all", response_model=list[UserSchema])
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
    modelUpdate: UserUpdate,
):
    return await rep.update_user(user_id, modelUpdate)

@user_router.delete("/delete")
async def delete_user(
    rep: Annotated[SQLAlchemyUserRepository, Depends(get_user_rep)],
    user_id: int,
):
    return await rep.delete_user(user_id)

@user_router.get("/tasks/{user_id}")
async def user_tasks(
    rep: Annotated[SQLAlchemyUserRepository, Depends(get_user_rep)],
    user_id: int,
):
    return await rep.user_task(user_id)