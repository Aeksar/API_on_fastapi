from fastapi import WebSocket, Depends, WebSocketDisconnect, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.api.schemas.user import UserFullSchema
from app.repositories.comm_repository import SQLAlchemyCommRepository
from app.db.database import get_async_session
from app.utils.endp_utils import ws_manager
from app.core.security import get_current_user
from app.api.schemas.comment import CommCreate

comm_router = APIRouter(prefix='/comments')

@comm_router.websocket('/ws/{task_id}')
async def ws_endpoint(ws: WebSocket, task_id: int):
    await ws_manager.connect(ws, task_id)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        await ws_manager.disconect(ws, task_id)

@comm_router.post('/{task_id}', status_code=201)
async def create_new_comm(
    comm: CommCreate,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    owner: Annotated[UserFullSchema, Depends(get_current_user)],
    task_id: int
):
    rep = SQLAlchemyCommRepository(session=session)
    new_comm = await rep.create_comm(comm=comm, username=owner.username, task_id=task_id)
    await ws_manager.send_comm(new_comm.f_task, new_comm.text, new_comm.owner)
    
    return new_comm

@comm_router.get('/{task_id}')
async def show_old_comm(
    task_id: int, 
    session: Annotated[AsyncSession, Depends(get_async_session)] 
):
    rep = SQLAlchemyCommRepository(session=session)
    return await rep.task_comms(task_id)
