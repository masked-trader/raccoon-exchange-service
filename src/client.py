import functools
import json

import ccxt
from pymongo import MongoClient

from constants import MONGO_CONNECTION_URL


@functools.cache
def get_ccxt_client(exchange: str, config: str, sandbox: bool = False) -> ccxt.Exchange:
    websocket_cls = getattr(ccxt, exchange)

    client: ccxt.Exchange = websocket_cls(json.loads(config))
    client.set_sandbox_mode(sandbox)

    return client


@functools.cache
def get_mongo_client() -> MongoClient:
    return MongoClient(MONGO_CONNECTION_URL)
