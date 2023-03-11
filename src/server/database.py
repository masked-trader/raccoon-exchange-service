import motor.motor_asyncio
from beanie import init_beanie

from server.models.balance import ExchangeBalance
from server.models.connection import ExchangeConnection, synchronize_redis_connections
from server.models.order import ExchangeOrder
from server.models.subscription import (
    ExchangeSubscription,
    synchronize_redis_subscriptions,
)
from settings import settings


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_connection_url)
    database = getattr(client, settings.mongo_database)

    await init_beanie(
        database=database,
        document_models=[
            ExchangeBalance,
            ExchangeConnection,
            ExchangeSubscription,
            ExchangeOrder,
        ],  # type: ignore
    )


async def init_redis():
    await synchronize_redis_connections()
    await synchronize_redis_subscriptions()
