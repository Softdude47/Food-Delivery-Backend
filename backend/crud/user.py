from fastapi import status
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.user import CreateUserSchema
from backend.model.user import User


async def create(payload: CreateUserSchema, session: AsyncSession) -> User:
    """
    Create a new user in the database. The function converts the provided CreateUserSchema payload into a User SQLAlchemy model, adds it to the database session, commits the transaction, and refreshes the object with its database-generated values.
    Args:
        payload (CreateUserSchema): The data used to create the new user.
        session (AsyncSession): The asynchronous SQLAlchemy database session.

    Returns: User: The newly created User SQLAlchemy model instance.
    """
    user = User(**payload.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def read(session: AsyncSession, **kwargs) -> User:
    """ Retrieve a user from the database based on the provided keyword arguments. The function constructs a SQLAlchemy select statement using the User model and filters it based on the provided criteria. If a user matching the criteria is found, it is returned; otherwise, an HTTP 404 Not Found exception is raised.
    Args:
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: Arbitrary keyword arguments used to filter the user query (e.g., username, email).

    Raises:
        HTTPException: Raises HTTP 404 Not Found if no user matching the provided criteria exists.

    Returns:
        User: The User SQLAlchemy model instance that matches the provided criteria.
    """
    statement = select(User).filter_by(**kwargs)

    user = await session.execute(statement)
    user = user.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with criteria {kwargs} not found")
    return user


async def update(username: str, payload: CreateUserSchema,
                 session: AsyncSession):
    """
    Update an existing user in the database. The function searches for a user using the username contained in the payload. If the user exists, the fields provided in the payload are applied to the existing database object. The changes are then committed and the updated object is refreshed.
    Args:
        user_id (str): The id of the user to be updated.
        payload (CreateUserSchema): The user data and the fields to be updated.
        session (AsyncSession): The asynchronous SQLAlchemy database session.

    Raises:
        HTTPException: Raises HTTP 404 Not Found if no user with the provided username exists.

    Returns:
        User: The updated User SQLAlchemy model instance.
    """
    statement = select(User).where(User.username == username)

    user = await session.execute(statement)
    user = user.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username {username} not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    await session.commit()
    await session.refresh(user)

    return user
