from fastapi import APIRouter
from backend.api.v1.user import user_router
from backend.api.v1.food import food_router

api = APIRouter(prefix="/api/v1")

api.include_router(router=user_router)
api.include_router(router=food_router)
