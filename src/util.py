import functools
import json

import ccxt
import requests

from client import get_ccxt_client
from constants import INTERNAL_CONFIG_API_URL


@functools.cache
def get_exchange_connection_config(connection_id: str) -> dict:
    return requests.get(f"{INTERNAL_CONFIG_API_URL}/connection/{connection_id}/").json()


@functools.cache
def get_exchange_client(connection_id: str) -> ccxt.Exchange:
    connection_config = get_exchange_connection_config(connection_id)

    sandbox = connection_config["sandbox"]
    exchange = connection_config["exchange"]

    client_config = {}

    if api_key := connection_config.get("apiKey"):
        client_config.update({"apiKey": api_key})

    if secret := connection_config.get("secret"):
        client_config.update({"secret": secret})

    if options := connection_config.get("options", {}):
        client_config.update({"options": options})

    return get_ccxt_client(
        exchange=exchange,
        config=json.dumps(client_config),
        sandbox=sandbox,
    )
