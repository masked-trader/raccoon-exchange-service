from typing import Optional
from uuid import uuid4

from beanie import Delete, Document, Insert, after_event
from pydantic import BaseModel, Field

from client import get_redis_client
from server.routes.balance import sync_balances
from server.routes.market import sync_markets

REDIS_CONNECTION_CONFIG_KEY = "connection-config"


async def synchronize_redis_connections():
    connections = await ExchangeConnection.find_all().to_list()

    for connection in connections:
        redis = get_redis_client()
        redis.sadd(REDIS_CONNECTION_CONFIG_KEY, connection.id)


class ExchangeConnection(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))
    exchange: str
    apiKey: str
    secret: str
    sandbox: Optional[bool] = False
    options: Optional[dict] = {}

    @after_event(Insert)
    async def sync_account_balances(self):
        await sync_balances(x_connection_id=self.id)

    @after_event(Insert)
    async def sync_client_markets(self):
        await sync_markets(x_connection_id=self.id)

    @after_event(Insert)
    def insert_redis_connection_config(self):
        redis = get_redis_client()
        redis.sadd(REDIS_CONNECTION_CONFIG_KEY, self.id)

    @after_event(Delete)
    def delete_redis_connection_config(self):
        redis = get_redis_client()
        redis.srem(REDIS_CONNECTION_CONFIG_KEY, self.id)

    class Settings:
        name = "exchange-connection"


class ExchangeConnectionView(BaseModel):
    id: str = Field(alias="_id")
    exchange: str
    sandbox: bool
    options: dict
