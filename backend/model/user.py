import uuid
from typing import List
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import relationship, mapped_column, Mapped, validates
from backend.model.address import Address
from backend.database.database import Base
from backend.auth.security import _hash_password, _verify_password


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(primary_key=True,
                                    default=lambda: uuid.uuid7().hex)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)

    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(150))

    address: Mapped[List["Address"]] = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now())
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 onupdate=datetime.now,
                                                 default=datetime.now)


    def check_password(self, input_password: str) -> bool:
        """ Checks if a password match with the user password hash
        Args:
            input_password (str): password string to compare database password hash
        Returns:
            True if the supplied password matches the password in database else False"""
        
        return _verify_password(self.password.encode("utf-8"), input_password)

    @validates("password")
    def password_hashing(self, key, value):
        """ Hashes password before saving to database """
        password_hash = _hash_password(value)
        return password_hash.decode(encoding="utf-8")