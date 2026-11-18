from sqlalchemy import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.model.order import Order, OrderItem
from backend.schemas.order import CreateOrderSchema, CreateOrderItemSchema, UpdateOrderSchema, UpdateOrderItemSchema


async def create_order(payload: CreateOrderSchema, session: AsyncSession):
    """
    Create a new order in the database. The function converts the provided CreateOrderSchema payload into an Order SQLAlchemy model, adds it to the database session, commits the transaction, and refreshes the object with its database-generated values.
    Args:
        payload (CreateOrderSchema): The data used to create the new order.
        session (AsyncSession): The asynchronous SQLAlchemy database session.

    Returns:
        Order: The newly created Order SQLAlchemy model instance.
    """
    new_order = Order(**payload.model_dump(exclude_unset=True))
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)
    return new_order


async def read_order(session: AsyncSession, **kwargs):
    """
    Retrieve orders from the database based on provided filter criteria. The function creates a SELECT query that filters orders based on the keyword arguments passed to it.
    Args:
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: Arbitrary keyword arguments representing filter criteria for the orders.

    Raises:
        HTTPException: Raises HTTP 404 Not Found if no orders matching the provided criteria are found.
    Returns:
        List[Order]: A list of Order SQLAlchemy model instances that match the filter criteria.
    """
    statement = select(Order).filter_by(**kwargs)
    result = await session.execute(statement)
    result = result.scalars().all()

    if len(result) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No orders found matching the criteria: {kwargs}")

    return result


async def update_order(session: AsyncSession, payload: UpdateOrderSchema,
                       **kwargs):
    """
    Update an existing order in the database. The function searches for an order using the provided keyword arguments. If the order exists, the fields provided in the payload are applied to the existing database object. The changes are then committed and the updated object is refreshed.
    Args:
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        payload (UpdateOrderSchema): The order data and the fields to be updated.
        **kwargs: Arbitrary keyword arguments representing filter criteria for the order to be updated.

    Raises:
        HTTPException: Raises HTTP 404 Not Found if no order with the provided ID exists.
    
    Returns:
        Order: The updated Order SQLAlchemy model instance.
    """
    statement = select(Order).filter_by(**kwargs)
    result = await session.execute(statement)
    result = result.one_or_none()

    for key, value in payload.model_dump(exclude_unset=True):
        setattr(result, key, value)

    await session.commit()
    await session.refresh(result)

    return result


async def delete_order(session: AsyncSession, **kwargs):
    """
    Delete an existing order from the database. The function searches for an order using the provided keyword arguments. If the order exists, it is deleted from the database and the changes are committed.
    Args:
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: Arbitrary keyword arguments representing filter criteria for the order to be deleted.
    Raises:
        HTTPException: Raises HTTP 404 Not Found if no order with the provided criteria exists.
    Returns:
        None
    """
    statement = select(Order).filter_by(**kwargs)
    result = await session.execute(statement)
    result = result.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No order matching the criteria {kwargs}")

    await session.delete(result)
    await session.commit()

    return


async def create_order_item(payload: CreateOrderItemSchema,
                            session: AsyncSession):
    """
    Create a new order item in the database. The function converts the provided CreateOrderItemSchema payload into an OrderItem SQLAlchemy model, adds it to the database session, commits the transaction, and refreshes the object with its database-generated values.
    Args:
        payload (CreateOrderItemSchema): The schema containing the data for the new order item.
        session (AsyncSession): The asynchronous SQLAlchemy database session.
    Returns:
        OrderItem: The created OrderItem SQLAlchemy model instance.
    """
    new_order_item = OrderItem(**payload.model_dump(exclude_unset=True))
    session.add(new_order_item)

    await session.commit()
    await session.refresh(new_order_item)

    return new_order_item


async def read_order_item(session: AsyncSession, **kwargs):
    """
    Retrieve an order item from the database based on provided filter criteria. The function creates a SELECT query that filters order items based on the keyword arguments passed to it.
    Args:
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: Arbitrary keyword arguments representing filter criteria for the order item to be retrieved.
    Raises:
        HTTPException: Raises HTTP 404 Not Found if no order item with the provided criteria exists.
    Returns:
        OrderItem: The retrieved OrderItem SQLAlchemy model instance.
    """
    statement = select(OrderItem).filter_by(**kwargs)
    result = await session.execute(statement)
    result = result.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No item matching the criteria {kwargs}")

    return result


async def update_order_item(payload: UpdateOrderItemSchema,
                            session: AsyncSession, **kwargs):
    """
    Update an existing order item in the database. The function searches for an order item using the provided keyword arguments. If the order item exists, the fields provided in the payload are applied to the existing database object. The changes are then committed and the updated object is refreshed.
    Args:
        payload (UpdateOrderItemSchema): The schema containing the updated data for the order item.
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: Arbitrary keyword arguments representing filter criteria for the order item to be updated.
    Raises:
        HTTPException: Raises HTTP 404 Not Found if no order item with the provided criteria exists.
    Returns:
        OrderItem: The updated OrderItem SQLAlchemy model instance.
    """
    statement = select(OrderItem).filter_by(**kwargs)
    result = await session.execute(statement)

    result = result.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No item matching the criteria {kwargs}")

    for key, value in payload.model_dump(exclude_unset=True):
        setattr(result, key, value)

    await session.commit()
    await session.refresh(result)

    return result


async def delete_order_item(session: AsyncSession, **kwargs):
    """
    Delete an existing order item from the database. The function searches for an order item using the provided keyword arguments. If the order item exists, it is deleted from the database and the changes are committed.
    Args:
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: Arbitrary keyword arguments representing filter criteria for the order item to be deleted.
    Raises:
        HTTPException: Raises HTTP 404 Not Found if no order item with the provided criteria exists.
    Returns:
        None
    """
    statement = select(OrderItem).filter_by(**kwargs)
    result = await session.execute(statement)
    result = result.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No item matching the criteria {kwargs}")

    await session.delete(result)
    await session.commit()

    return
