from fastapi import APIRouter, Depends
from app.core.security import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
async def admin_dashboard(
    user=Depends(require_role("admin")),
):
    return {"message": "Welcome admin"}
