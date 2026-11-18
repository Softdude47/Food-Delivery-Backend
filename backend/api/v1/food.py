from typing import Annotated
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.database import DbSession
from backend.schemas.food import CreateFoodSchema, FoodSchema, CategorySchema, CreateCategorySchema
from backend.crud.food import create_food_db, get_food_db, update_food_db, get_food_category_db, create_food_category_db, update_food_category_db

food_router = APIRouter(prefix="/food")


@food_router.post("/", response_model=FoodSchema)
async def create(payload: CreateFoodSchema, session: DbSession):
    new_food = await create_food_db(payload, session)
    return new_food


@food_router.get("/{id}", response_model=FoodSchema)
async def get_food(id: int, session: DbSession):
    existing_food = await get_food_db(session, id=id)
    return existing_food


@food_router.put("/{id}", response_model=FoodSchema)
async def update_food(id: int, payload: CreateFoodSchema, session: DbSession):
    updated_food = await update_food_db(payload, session, id=id)
    return updated_food


@food_router.get("/categories/{id}", response_model=CategorySchema)
async def get_food_category(id: int, session: DbSession):
    existing_category = await get_food_category_db(id=id, session=session)
    return existing_category


@food_router.post("/categories", response_model=CategorySchema)
async def create_food_category(payload: CreateCategorySchema,
                               session: DbSession):
    new_food_category = await create_food_category_db(payload=payload,
                                                      session=session)
    return new_food_category


@food_router.put("categories/{id}", response_class=CategorySchema)
async def update_food_category(id: int, payload: CreateCategorySchema,
                               session: DbSession):
    updated_food_category = update_food_category_db(payload=payload,
                                                    session=session,
                                                    id=id)
    return updated_food_category
