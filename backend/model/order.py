import uuid
from typing import List
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, ForeignKey, Integer, Numeric, DateTime, func, JSON
from backend.model.food import Food
from backend.model.user import Address, User
from backend.database.database import Base, DeliveryStatus, PaymentStatus


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(primary_key=True,
                                    default=lambda: uuid.uuid7().hex)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"),
                                         nullable=False)
    delivery_address_id: Mapped[str] = mapped_column(
        ForeignKey("addresses.id"), nullable=False)

    delivery_status: Mapped[DeliveryStatus] = mapped_column(
        Enum(DeliveryStatus, native_enum=False),
        default=DeliveryStatus.PENDING,
        nullable=False)

    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, native_enum=False),
        default=PaymentStatus.PENDING,
        nullable=False)

    delivery_address: Mapped[Address] = relationship("Address")
    address_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)

    total_price: Mapped[Decimal] = mapped_column(Numeric(precision=10,
                                                         scale=2),
                                                 nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 onupdate=func.now())

    user: Mapped[User] = relationship("User")
    items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[str] = mapped_column(primary_key=True,
                                    default=lambda: uuid.uuid7().hex)

    food_id: Mapped[str] = mapped_column(ForeignKey("foods.id"),
                                         nullable=False)

    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"),
                                          nullable=False)

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2),
                                                nullable=False)

    food: Mapped[Food] = relationship("Food")
    order: Mapped[Order] = relationship("Order", back_populates="items")
