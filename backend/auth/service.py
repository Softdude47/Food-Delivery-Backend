from backend.crud.user import read, create
from backend.database.database import DbSession
from backend.schemas.user import CreateUserSchema, UserSchema, AccessToken
from backend.auth.security import verify_password, encode_token


async def authenticate_user(username: str, password: str,
                            session: DbSession) -> dict:
    """Authenticates the user by verifying the username and password against the database."""
    existing_user = await read(username=username, session=session)
    if not existing_user or not existing_user.check_password(input_password=password):
        return None
    
    payload = {"username": username}
    token = AccessToken(token=encode_token(payload)).model_dump()
    
    user_schema = UserSchema.model_validate(existing_user)
    user_schema.token = token
    return user_schema.model_dump()


async def register_user(payload: CreateUserSchema, session: DbSession):
    new_user = await create(payload, session)
    token = encode_token({"username": new_user.username})
    token = AccessToken.model_validate(token).model_dump()

    new_user_schema = UserSchema.model_validate(new_user).model_dump()
    new_user_schema = new_user_schema.update({"token": token})

    return new_user_schema