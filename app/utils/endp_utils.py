from fastapi import WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.repositories.task_repository import SQLAlchemyTaskRepository
from app.db.database import get_async_session


async def get_task_rep(session: Annotated[AsyncSession, Depends(get_async_session)]) -> SQLAlchemyTaskRepository:
    return SQLAlchemyTaskRepository(session=session)

class ConnectionManager:
    def __init__(self):
        self.active_conn: dict = {}
        
    async def connect(self, ws: WebSocket, task_id: int):
        try:
            await ws.accept()
            if task_id not in self.active_conn:
                self.active_conn[task_id] = []
            self.active_conn[task_id].append(ws)
        except Exception as e:
            print(e)
        
    async def disconect(self, ws: WebSocket, task_id: int):
        try:
            if task_id in self.active_conn:
                self.active_conn[task_id].remove(ws)
                if not self.active_conn[task_id]:
                    del self.active_conn[task_id]
        except Exception as e:
            print(e)
        
    async def send_comm(self, task_id: int, text: str, owner: str):
        try:
            if task_id in self.active_conn:
                for conn in self.active_conn[task_id]:
                    await conn.send_json({'user': owner, 'text': text})
        except Exception as e:
            print(e)
                
ws_manager = ConnectionManager()