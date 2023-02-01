import functools

import requests

from constants import INTERNAL_CONFIG_API_URL


@functools.cache
def internal_retrieve_connection_config(connection_id: str) -> dict:
    return requests.get(f"{INTERNAL_CONFIG_API_URL}/connection/{connection_id}/").json()
