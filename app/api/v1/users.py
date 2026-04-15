from fastapi import APIRouter, Depends
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
async def get_me(user_id: str = Depends(get_current_user)):
    return {"user_id" : user_id}
