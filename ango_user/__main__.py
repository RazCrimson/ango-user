from ango_user.app.core.config import Settings
from fastapi import FastAPI
from ango_user.app.routers.user import user_router
import uvicorn

settings = Settings()

app = FastAPI()

app.include_router(user_router, prefix="/user")

uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
