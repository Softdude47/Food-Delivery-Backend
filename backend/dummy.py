from backend.database.database import local_session
from backend.schemas.user import UserSchema, CreateUserSchema
from backend.crud.user import update
import asyncio

dummy_users = [
    {
        "id": "01",
        "is_superuser": False,
        "is_admin": False,
        "first_name": "John",
        "last_name": "Okafor",
        "phone": "08031234567",
        "email": "john.okafor@example.com",
        "username": "johnokafor",
        "password": "password123",
    },
    {
        "id": "02",
        "is_superuser": False,
        "is_admin": False,
        "first_name": "Mary",
        "last_name": "Eze",
        "phone": "08142345678",
        "email": "mary.eze@example.com",
        "username": "maryeze",
        "password": "password123",
    },
    {
        "id": "03",
        "is_superuser": False,
        "is_admin": False,
        "first_name": "David",
        "last_name": "Adeyemi",
        "phone": "07053456789",
        "email": "david.adeyemi@example.com",
        "username": "davidadeyemi",
        "password": "password123",
    },
    {
        "id": "04",
        "is_superuser": False,
        "is_admin": False,
        "first_name": "Sarah",
        "last_name": "Williams",
        "phone": "09064567890",
        "email": "sarah.williams@example.com",
        "username": "sarahwilliams",
        "password": "password123",
    },
    {
        "id": "05",
        "is_superuser": False,
        "is_admin": False,
        "first_name": "Michael",
        "last_name": "Okoro",
        "phone": "08075678901",
        "email": "michael.okoro@example.com",
        "username": "michaelokoro",
        "password": "password123",
    },
    {
        "id": "06",
        "is_superuser": False,
        "is_admin": False,
        "first_name": "Grace",
        "last_name": "Ibrahim",
        "phone": "08186789012",
        "email": "grace.ibrahim@example.com",
        "username": "graceibrahim",
        "password": "password123",
    },
    {
        "id": "07",
        "is_superuser": False,
        "is_admin": False,
        "first_name": "Daniel",
        "last_name": "Chukwu",
        "phone": "07097890123",
        "email": "daniel.chukwu@example.com",
        "username": "danielchukwu",
        "password": "password123",
    },
    {
        "id": "08",
        "is_superuser": False,
        "is_admin": False,
        "first_name": "Esther",
        "last_name": "Bassey",
        "phone": "09108901234",
        "email": "esther.bassey@example.com",
        "username": "estherbassey",
        "password": "password123",
    },
    {
        "id": "09",
        "is_superuser": False,
        "is_admin": False,
        "first_name": "Samuel",
        "last_name": "Nwosu",
        "phone": "08019012345",
        "email": "samuel.nwosu@example.com",
        "username": "samuelnwosu",
        "password": "password123",
    },
    {
        "id": "10",
        "is_superuser": False,
        "is_admin": False,
        "first_name": "Blessing",
        "last_name": "Udo",
        "phone": "08120123456",
        "email": "blessing.udo@example.com",
        "username": "blessingudo",
        "password": "password123",
    },
]

dummy_addresses = [
    {
        "id": 1,
        "user_id": "01",
        "street": "12 Aba Road",
        "city": "Port Harcourt",
        "state": "Rivers",
    },
    {
        "id": 2,
        "user_id": "02",
        "street": "25 Ikwerre Road",
        "city": "Port Harcourt",
        "state": "Rivers",
    },
    {
        "id": 3,
        "user_id": "03",
        "street": "18 Airport Road",
        "city": "Benin City",
        "state": "Edo",
    },
    {
        "id": 4,
        "user_id": "04",
        "street": "7 Admiralty Way",
        "city": "Lekki",
        "state": "Lagos",
    },
    {
        "id": 5,
        "user_id": "05",
        "street": "31 GRA Road",
        "city": "Enugu",
        "state": "Enugu",
    },
    {
        "id": 6,
        "user_id": "06",
        "street": "14 Ahmadu Bello Way",
        "city": "Kaduna",
        "state": "Kaduna",
    },
    {
        "id": 7,
        "user_id": "07",
        "street": "22 Nnamdi Azikiwe Street",
        "city": "Onitsha",
        "state": "Anambra",
    },
    {
        "id": 8,
        "user_id": "08",
        "street": "9 Ewet Housing Estate",
        "city": "Uyo",
        "state": "Akwa Ibom",
    },
    {
        "id": 9,
        "user_id": "09",
        "street": "16 Independence Avenue",
        "city": "Abuja",
        "state": "FCT",
    },
    {
        "id": 10,
        "user_id": "10",
        "street": "42 Marian Road",
        "city": "Calabar",
        "state": "Cross River",
    },
]


async def main():
    async with local_session() as session:
        from backend.model.user import User
        from sqlalchemy import select
        statement = select(User).where(User.is_admin==False)
        users = await session.execute(statement)
        for u in users.scalars().all():
            u.password = "Imakpokpomwan47"
        
        await session.commit()


asyncio.run(main())
