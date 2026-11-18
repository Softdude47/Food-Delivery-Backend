from fastapi import FastAPI
from backend.api.api import api
from backend.model.user import User, Address
from backend.model.food import Food, Category
from backend.model.order import Order, OrderItem
from backend.database.database import engine, Base
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router=api)
