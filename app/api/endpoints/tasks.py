from fastapi import APIRouter, Depends, status
from typing import Annotated, List

from app.api.schemas.task import TaskSchemas, TaskCreate
from app.repositories.task_repository import SQLAlchemyTaskRepository
from app.db.models import Task
from app.api.endpoints.comments import ws_manager
from app.api.schemas.user import UserFullSchema
from app.core.security import get_current_user
from app.utils.endp_utils import get_task_rep


task_router = APIRouter(prefix="/task")


@task_router.get("/all", response_model=List[TaskSchemas])
async def get_all_task(rep: Annotated[SQLAlchemyTaskRepository, Depends(get_task_rep)]):
    return await rep.get_tasks()


@task_router.get('/{task_id}')
async def get_one_task(
    rep: Annotated[SQLAlchemyTaskRepository, Depends(get_task_rep)],
    task_id: int,
    ):
    return await rep.get_task(task_id)


@task_router.post('/new', status_code=status.HTTP_201_CREATED)
async def create_task(
rep: Annotated[SQLAlchemyTaskRepository, Depends(get_task_rep)],
user: Annotated[UserFullSchema, Depends(get_current_user)],
new_task: TaskCreate
):
    return await rep.create_task(new_task, user.id)



    
