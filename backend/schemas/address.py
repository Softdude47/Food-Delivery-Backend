from pydantic import BaseModel, Field, ConfigDict


class AddressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str
    user_id: str
    street: str
    city: str
    state: str
    country: str


class CreateAddressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str | None = Field(default=None)
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)


class UpdateAddressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    country: str | None = Field(default=None)
