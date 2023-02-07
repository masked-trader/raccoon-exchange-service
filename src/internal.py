import functools

import requests

from settings import settings


@functools.cache
def internal_retrieve_connection_config(connection_id: str) -> dict:
    return requests.get(
        f"{settings.internal_api_base_url}/internal/config/connection/{connection_id}/",
        verify=settings.internal_ssl_verify,
    ).json()
