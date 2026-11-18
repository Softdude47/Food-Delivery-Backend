from fastapi import APIRouter, Depends

from backend.database.database import DbSession
from backend.crud.user import read, create, update
from backend.schemas.user import CreateUserSchema, UserSchema, AccessToken
from backend.auth.service import authenticate_user, register_user

user_router = APIRouter(prefix="/user")


@user_router.get("/{username}", response_model=UserSchema)
async def get_user(username: str, session: DbSession) -> UserSchema:
    user = await read(username=username, session=session)
    return user


@user_router.post("/login", response_model=UserSchema)
async def login(username: str, password: str, session: DbSession):
    serialized_user_and_token = await authenticate_user(
        username, password, session)
    return serialized_user_and_token


@user_router.post("/signup", response_model=UserSchema)
async def signup_user(payload: CreateUserSchema,
                      session: DbSession) -> UserSchema:
    # user = await create(payload=payload, session=session)
    # serialized_user = UserSchema.model_validate(user).model_dump()

    return register_user(payload, session)


@user_router.put("/{username}", response_model=UserSchema)
async def edit_user(username, payload: CreateUserSchema,
                    session: DbSession) -> UserSchema:
    updated_user = await update(username=username,
                                payload=payload,
                                session=session)

    return updated_user
