import functools

import ccxt
import redis
from pymongo import MongoClient

from settings import settings


@functools.cache
def get_redis_client() -> redis.Redis:
    return redis.Redis.from_url(settings.redis_connection_url)


@functools.cache
def get_mongo_client():
    return MongoClient(settings.mongo_connection_url)


@functools.cache
def get_mongo_database():
    client = get_mongo_client()
    return client[settings.mongo_database]


@functools.cache
def get_mongo_collection(collection: str):
    db = get_mongo_database()
    return db[collection]


@functools.cache
def get_ccxt_client(connection_id: str) -> ccxt.Exchange:
    collection = get_mongo_collection("exchange-connection")
    connection = collection.find_one({"_id": connection_id})

    if not connection:
        raise ValueError("connection configuration not found")

    sandbox_mode = connection["sandbox"]
    exchange_name = connection["exchange"]

    exchange_cls = getattr(ccxt, exchange_name)

    client_config = {"options": connection.get("options", {})}

    if api_key := connection.get("apiKey"):
        client_config.update({"apiKey": api_key})

    if secret := connection.get("secret"):
        client_config.update({"secret": secret})

    client: ccxt.Exchange = exchange_cls(client_config)
    client.set_sandbox_mode(sandbox_mode)

    return client
