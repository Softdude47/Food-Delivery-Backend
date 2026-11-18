from typing import List
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Boolean, DateTime, func, ForeignKey, Numeric

from backend.database.database import Base


class Food(Base):
    __tablename__ = "foods"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("food_categories.id"))
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    category: Mapped[Category] = relationship("Category",
                                              back_populates="foods")
    description: Mapped[str] = mapped_column(String(30))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    image: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 onupdate=datetime.now)


class Category(Base):
    __tablename__ = "food_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    foods: Mapped[List[Food]] = relationship("Food", back_populates="category")
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
