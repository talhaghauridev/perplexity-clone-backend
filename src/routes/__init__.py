from fastapi import APIRouter
from .users import users

router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(users)

__all__ = ["router"]
