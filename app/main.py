from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as user_router
from app.api.v1.admin import router as admin_router

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)


'''
@app.get("/health")
async def health_check():
    return {"status"  :"ok"}
'''