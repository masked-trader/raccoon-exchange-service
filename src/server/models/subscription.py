from enum import Enum
from typing import Optional

from beanie import Delete, Document, Insert, after_event

from client import get_redis_client
from server.models.connection import ExchangeConnection


class ExchangeSubscriptionType(Enum):
    KLINE = "kline"
    TICKER = "ticker"


class ExchangeSubscription(Document):
    type: ExchangeSubscriptionType
    symbol: str
    interval: Optional[str]
    connection: Optional[str]

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
    if subscription.type == ExchangeSubscriptionType.TICKER:
        return subscription.symbol

    elif subscription.type == ExchangeSubscriptionType.KLINE:
        return "-".join([subscription.symbol, subscription.interval])  # type: ignore

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
