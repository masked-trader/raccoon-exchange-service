import logging

import uvicorn

from constants import SERVICE_HOST, SERVICE_LOG_LEVEL, SERVICE_PORT, SERVICE_RELOAD

logging.basicConfig(
    level=getattr(logging, SERVICE_LOG_LEVEL),
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

if __name__ == "__main__":
    uvicorn.run(
        "server.app:app", host=SERVICE_HOST, port=SERVICE_PORT, reload=SERVICE_RELOAD
    )
