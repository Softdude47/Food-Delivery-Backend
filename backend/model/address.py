from backend.database.database import Base
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.model.user import User


class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    street: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(30))
    state: Mapped[str] = mapped_column(String(30))
    user: Mapped["User"] = relationship("User",
                                        back_populates="address",
                                        cascade="all, delete")
