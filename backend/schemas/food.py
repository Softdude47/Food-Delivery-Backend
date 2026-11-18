from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class FoodSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str
    name: str
    description: str
    image: str | None
    price: float
    is_availabel: bool
    updated_at: datetime


class CreateFoodSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    image: str | None
    price: float
    is_availabel: bool


class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)
    id: str
    name: str
    foods: List[FoodSchema] | None


class CreateCategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
