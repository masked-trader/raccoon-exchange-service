import motor.motor_asyncio
from beanie import init_beanie

from server.models.balance import ExchangeBalance
from server.models.order import ExchangeOrder
from settings import settings


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_connection_url)
    database = getattr(client, settings.mongo_database)

    await init_beanie(
        database=database,
        document_models=[ExchangeOrder, ExchangeBalance],  # type: ignore
    )
