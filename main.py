import uvicorn
from fastapi import FastAPI

from app.api.endpoints.tasks import task_router
from app.api.endpoints.users import user_router

app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)

print("app working")
# if __name__ == "__main__":
#     
#     uvicorn.run(app="main:app", host = "0.0.0.0", port = 8001)