from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    is_superuser: bool
    first_name: str
    last_name: str

    email: EmailStr
    username: str
    phone: str

    created_at: datetime
    last_login: datetime

    token: "AccessToken | None" = Field(default=None)


class CreateUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    is_superuser: bool | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)

    email: EmailStr | None = Field(default=None)
    username: str | None = Field(default=None)
    phone: str | None = Field(default=None)

    password: str | None = Field(default=None)



class AccessToken(BaseModel):
    token_type: str = Field(default="bearer")
    token: str
