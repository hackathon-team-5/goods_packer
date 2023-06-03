from fastapi import APIRouter

from .auth import routers

router = APIRouter()

router.include_router(routers.router, prefix="/users", tags=["users"])
