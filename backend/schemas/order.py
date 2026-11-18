from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from backend.model.user import Address, User
from backend.schemas.food import FoodSchema
from backend.schemas.user import UserSchema
from backend.database.database import DeliveryStatus, PaymentStatus


class OrderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    total_price: str

    delivery_status: DeliveryStatus
    payment_status: PaymentStatus
    delivery_address: Address
    address_snapshot: dict

    created_at: datetime
    updated_at: datetime

    user: UserSchema
    items: List[OrderItemSchema | None]


class CreateOrderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    total_price: str
    delivery_address_id: str

    delivery_status: DeliveryStatus | None
    payment_status: PaymentStatus | None

    delivery_address: Address
    address_snapshot: dict | None

    user: User
    items: List[OrderItemSchema | None]


class UpdateOrderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total_price: str | None

    delivery_status: DeliveryStatus | None
    payment_status: PaymentStatus | None

    delivery_address: Address | None
    address_snapshot: dict | None

    items: List[OrderItemSchema] | None


class OrderItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str | None
    order_id: str | None
    food_id: str | None
    food: FoodSchema | None
    quantity: int | None
    unit_price: str | None


class CreateOrderItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: str
    food_id: str
    quantity: int
    unit_price: float


class UpdateOrderItemSchema(BaseModel):
    quantity: int | None
    unit_price: str | None
