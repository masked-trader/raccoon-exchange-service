import functools

import ccxt
import redis

from internal import internal_retrieve_connection_config
from settings import settings


@functools.cache
def get_ccxt_client(connection_id: str) -> ccxt.Exchange:
    config = internal_retrieve_connection_config(connection_id)

    sandbox = config["sandbox"]
    exchange = config["exchange"]

    websocket_cls = getattr(ccxt, exchange)

    client_config = {}

    if api_key := config.get("apiKey"):
        client_config.update({"apiKey": api_key})

    if secret := config.get("secret"):
        client_config.update({"secret": secret})

    if options := config.get("options", {}):
        client_config.update({"options": options})

    client: ccxt.Exchange = websocket_cls(client_config)
    client.set_sandbox_mode(sandbox)

    return client


@functools.cache
def get_redis_client() -> redis.Redis:
    return redis.Redis.from_url(settings.redis_connection_url)
