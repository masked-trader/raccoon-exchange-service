import motor.motor_asyncio
from beanie import init_beanie

from constants import MONGO_CONNECTION_URL, MONGO_DATABASE
from server.models.balance import ExchangeBalance
from server.models.order import ExchangeOrder


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION_URL)
    database = getattr(client, MONGO_DATABASE)

    await init_beanie(
        database=database,
        document_models=[ExchangeOrder, ExchangeBalance],  # type: ignore
    )
