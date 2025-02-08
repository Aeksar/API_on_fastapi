from fastapi import APIRouter
from schemas.user import User

rout = APIRouter()

@rout.get('/info/{id}')
async def user_info(id: int):
    #search user in db
    pass
