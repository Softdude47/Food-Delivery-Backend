from enum import StrEnum
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import DeclarativeBase
from backend.database.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

import os
class Base(DeclarativeBase):
    pass


class DeliveryStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    OUT_FOR_DELIVERY = "out for delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


engine = create_async_engine(url=settings.DATABASE_URL, echo=True)
local_session = async_sessionmaker(bind=engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)


async def get_db():
    async with local_session() as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_db)]
