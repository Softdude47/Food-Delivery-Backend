import jwt
import bcrypt
import asyncio
from fastapi import status
from fastapi.exceptions import HTTPException
from backend.database.config import settings


def _hash_password(password: str) -> bytes:
    """Hashes the password using bcrypt and returns the hashed password."""
    salt = bcrypt.gensalt(rounds=settings.SALT_ROUNDS)
    password_byte = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password=password_byte, salt=salt)
    return hashed_password


def _verify_password(hashed_password: bytes, input_password: str) -> bool:
    """Compares the hashed password with the input password and returns True if they match, False otherwise."""
    return bcrypt.checkpw(hashed_password=hashed_password,
                          password=input_password.encode("utf-8"))


async def hash_password(password: str) -> str:
    """Hashes the password asynchronously using bcrypt and returns the hashed password."""
    loop = asyncio.get_running_loop()
    return loop.run_in_executor(None, _hash_password, password)


async def verify_password(hashed_password: str, input_password: str) -> bool:
    """Compares the hashed password with the input password asynchronously and returns True if they match, False otherwise."""
    loop = asyncio.get_running_loop()
    return loop.run_in_executor(None, _verify_password, hashed_password,
                                input_password)


def encode_token(payload: dict) -> str:
    """Generates a JWT token for the payload and returns the token."""
    payload = {"sub": payload, "exp": settings.JWT_EXPIRATION_TIME}
    token = jwt.encode(payload=payload,
                       key=settings.SECRET_KEY,
                       algorithm=settings.ALGORITHM)

    return token


def decode_token(token: str):
    """Decodes the JWT token and returns the payload."""
    try:
        payload = jwt.decode(token,
                             key=settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired authentication token.")
    return payload
