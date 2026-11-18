from typing import List
from fastapi import status
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.model.food import Food, Category
from backend.schemas.food import FoodSchema, CategorySchema, CreateCategorySchema


async def create_food_db(payload: FoodSchema, session: AsyncSession) -> Food:
    """
    Creates a new food in the database. The function converts the provided FoodSchema payload into an SQLAlchemy model, adds it to the database session, commits the transaction, and refreshes the object with it database-generated values.
    Args:
        payload (FoodSchema): The data used to create the new food.
        session (AsynSession): The asynchronous SQLAlchemy database session.
    Returns:
        Food: The newly created SQLAlchemy model instance.
    """
    new_meal = Food(**payload.model_dump())
    session.add(new_meal)
    await session.commit()
    await session.refresh(new_meal)
    return new_meal


async def get_food_db(session: AsyncSession, **kwargs):
    """
    Retrieve a food from the database based on provided keyword arguments. The function creates a SELECT query that searches for a food matching the provided criteria.
    Args:
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: Arbitrary keyword arguments representing the search criteria for the food.
    Returns:
        List[Food]: A list of matching Food SQLAlchemy model instances.
    """
    statement = select(Food).filter_by(**kwargs)
    food = await session.execute(statement)

    return food.scalars().all()


async def update_food_db(payload: FoodSchema, session: AsyncSession, **kwargs):
    """
    Update an existing food in the database. The function searches for a food using the provided keyword arguments. If the food exists, the fields provided in the payload are applied to the existing database object. The changes are then committed and the updated object is refreshed.
    Args:
        payload (FoodSchema): The food data and the fields to be updated.
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: Arbitrary keyword arguments representing the search criteria for the food to be updated.
    Raises:
        HTTPException: Raises HTTP 404 Not Found if no food matching the provided criteria exists.
    Returns:
        Food: The updated Food SQLAlchemy model instance.
    """
    statement = select(Food).filter_by(**kwargs)
    food = await session.execute(statement)
    food = food.scalar_one_or_none()

    if food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Food with ID {payload.id} not found.")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(food, key, value)

    await session.commit()
    await session.refresh(food)

    return food


async def delete_food_db(session: AsyncSession, **kwargs):
    """
    Delete an existing food from the database. The function searches for a food using the provided keyword arguments. If the food exists, it is deleted from the database and the changes are committed.
    Args:
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: Arbitrary keyword arguments representing the search criteria for the food to be deleted.
    Raises:
        HTTPException: Raises HTTP 404 Not Found if no food matching the provided criteria exists.
    Returns:
        None
    """
    statement = select(Food).filter_by(**kwargs)
    food = await session.execute(statement)
    food = food.scalar_one_or_none()

    if food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Food with ID {id} not found")

    await session.delete(food)
    await session.commit()

    return


################## CATEGORIES ############################


async def get_food_category_db(session: AsyncSession, **kwargs):
    """
    Retrieve a food category from the database based on provided keyword arguments. The function creates a SELECT query that searches for a food category matching the provided criteria.
    Args:
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: Arbitrary keyword arguments representing the search criteria for the food category.
    Returns:
        List[Food]: A list of matching Food SQLAlchemy model instances.
    """
    statement = select(Category).filter_by(**kwargs)
    existing_category = await session.execute(statement)
    existing_category = existing_category.scalar_one_or_none()

    if existing_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with criteria {kwargs} not found")

    return existing_category


async def create_food_category_db(payload: CategorySchema,
                                  session: AsyncSession):
    """
    Creates a new food category in the database. The function converts the provided CategorySchema payload into an SQLAlchemy model, adds it to the database session, commits the transactions, and refreshes the object with its database-generated values.
    Args:
        payload (CategorySchema): The data used to create the new food category.
        session (AsyncSession): The asynchronous SQLAlchemy database session.
    return:
        FoodCategory: The newly created food category
    """
    new_category = Category(**payload.model_dump())
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)

    return new_category


async def update_food_category_db(payload: CategorySchema,
                                  session: AsyncSession, **kwargs):
    """
    Updates an existing food category in database. The funtion searches for an existing food category based on provided keyword arguments. If the food category exists, the fields in provided payload are then applied to the existing database object. The changes are then committed and the updated object is refreshed.
    Args:
        payload (CategorySchema): The data used to update the model instance.
        session (AsyncSession): The asynchronous SQLAlchemy database session.
        **kwargs: The keywords arguments used for finding the food model instance from database.
    Raises:
        HTTPException: Raises HTTP 404 Not Found if no food category matches the provided criteria.
    Returns:
        FoodCategory: The updated food category
    """
    statement = select(Category).filter_by(**kwargs)
    existing_category = await session.execute(statement)
    existing_category = existing_category.scalar_one_or_none()

    if existing_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with ID {payload.id} not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(existing_category, key, value)

    await session.commit()
    await session.refresh(existing_category)

    return existing_category
