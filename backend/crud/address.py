from sqlalchemy import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.address import AddressSchema, CreateAddressSchema, UpdateAddressSchema
from backend.model.user import Address


async def create(payload: CreateAddressSchema,
                 session: AsyncSession) -> Address:
    """
    Create a new address in the database. The function converts the provided CreateAddressSchema payload into an Address SQLAlchemy model, adds it to the database session, commits the transaction, and refreshes the object with its database-generated values.
    Args:
        payload (CreateAddressSchema): The data used to create the new address.
        session (AsyncSession): The asynchronous SQLAlchemy database session.

    Returns:
        Address: The newly created Address SQLAlchemy model instance.
    """
    address = Address(**payload.model_dump())
    session.add(address)
    await session.commit()
    await session.refresh(address)
    return address


async def read(session: AsyncSession, **kwargs) -> Address:
    """
    Retrieve an address from the database based on provided keyword arguments. The function creates a SELECT query that searches for an address matching the provided criteria.
    Args:
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: Arbitrary keyword arguments representing the search criteria for the address.
    Returns:
        Address: The matching Address SQLAlchemy model instance.
    """
    statement = select(Address).filter_by(**kwargs)
    result = await session.execute(statement)
    result = result.scalars().first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Address not found")

    return result


async def update(payload: AddressSchema, session: AsyncSession,
                 **kwargs) -> Address:
    """
    Update an existing address in the database. The function searches for an address using the provided keyword arguments. If the address exists, the fields provided in the payload are applied to the existing database object. The changes are then committed and the updated object is refreshed.
    Args:
        payload (AddressSchema): The address data and the fields to be updated.
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: Arbitrary keyword arguments representing the search criteria for the address to be updated.
    Raises:
        HTTPException: Raises HTTP 404 Not Found if no address matching the provided criteria exists.
    Returns:
        Address: The updated Address SQLAlchemy model instance.
    """

    statement = select(Address).filter_by(**kwargs)
    result = await session.execute(statement=statement)
    result = result.scalars().first()

    if result is None:
        kwargs_str = [f"{key} = {value}" for (key, value) in kwargs.items()]
        kwargs_str = ", ".join(kwargs_str)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"address where {kwargs_str}")

    for key, value in payload.model_dump(exclude_unset=True):
        setattr(result, key, value)

    await session.commit()
    await session.refresh(result)
    return result
