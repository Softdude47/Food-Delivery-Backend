from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from backend.crud.user import read
from backend.model.user import User
from backend.auth.security import decode_token
from backend.database.database import DbSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
jwt_token = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: jwt_token, session: DbSession) -> User:
    payload = decode_token(token)["sub"]
    user = await read(session, **payload)

    return user


async def is_admin_user(token: jwt_token, session: DbSession) -> bool:
    payload = decode_token(token)["sub"]
    user = await read(session, **payload)

    return user.is_admin

