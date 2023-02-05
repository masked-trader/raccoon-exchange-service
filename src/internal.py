import functools

import requests

from constants import INTERNAL_API_BASE_URL, INTERNAL_SSL_VERIFY


@functools.cache
def internal_retrieve_connection_config(connection_id: str) -> dict:
    return requests.get(
        f"{INTERNAL_API_BASE_URL}/internal/config/connection/{connection_id}/",
        verify=INTERNAL_SSL_VERIFY,
    ).json()
