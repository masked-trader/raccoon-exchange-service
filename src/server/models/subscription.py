from enum import Enum
from typing import Optional

from beanie import Delete, Document, Insert, after_event, before_event
from pydantic import BaseModel

from client import get_ccxt_client, get_redis_client
from server.models.connection import ExchangeConnection


class ExchangeSubscriptionType(Enum):
    KLINE = "kline"
    TICKER = "ticker"


class ExchangeTickerSubscriptionRequest(BaseModel):
    symbol: str


class ExchangeKlineSubscriptionRequest(BaseModel):
    symbol: str
    interval: str


class ExchangeSubscription(Document):
    type: ExchangeSubscriptionType
    connection: str
    symbol: str
    interval: Optional[str]

    @before_event(Insert)
    def validate_market_symbol(self):
        client = get_ccxt_client(self.connection)

        if self.symbol not in client.load_markets():
            raise ValueError(
                f"invalid symbol {self.symbol} for connection configuration"
            )

    @before_event(Insert)
    def validate_market_interval(self):
        if not self.interval:
            return

        client = get_ccxt_client(self.connection)
        client_properties = client.describe()

        if self.interval not in client_properties["timeframes"]:
            raise ValueError(f"invalid value for interval {self.interval}")

    @after_event(Insert)
    async def insert_subscription(self):
        connection = await ExchangeConnection.get(self.connection)  # type: ignore

        redis_key = get_redis_subscription_key(connection, self.type)  # type: ignore
        redis_value: str = get_redis_subscription_value(self)

        redis = get_redis_client()
        redis.sadd(redis_key, redis_value)

    @after_event(Delete)
    async def delete_subscription(self):
        connection = await ExchangeConnection.get(self.connection)  # type: ignore

        redis_key = get_redis_subscription_key(connection, self.type)  # type: ignore
        redis_value: str = get_redis_subscription_value(self)

        redis = get_redis_client()
        redis.srem(redis_key, redis_value)

    class Settings:
        name = "exchange-subscription"
        use_enum_values = True


def get_redis_subscription_key(
    connection: ExchangeConnection, sub_type: ExchangeSubscriptionType
):
    connection_name = (
        "-".join([connection.exchange, "sandbox"])
        if connection.sandbox
        else connection.exchange
    )

    return "-".join([connection_name, sub_type.value, "subs"])


def get_redis_subscription_value(subscription: ExchangeSubscription):
    client = get_ccxt_client(subscription.connection)

    markets = client.load_markets()
    market = markets[subscription.symbol]

    if subscription.type == ExchangeSubscriptionType.TICKER:
        return market["id"]

    elif subscription.type == ExchangeSubscriptionType.KLINE:
        return "-".join([market["id"], subscription.interval])  # type: ignore

    raise ValueError(f"invalid subscription type - {subscription.type.value}")


async def synchronize_redis_subscriptions():
    connections = await ExchangeConnection.find_all().to_list()

    for connection in connections:
        subscriptions = await ExchangeSubscription.find(
            ExchangeSubscription.connection == connection.id
        ).to_list()

        for subscription in subscriptions:
            redis_key = get_redis_subscription_key(connection, subscription.type)
            redis_value: str = get_redis_subscription_value(subscription)

            redis = get_redis_client()
            redis.sadd(redis_key, redis_value)
