import logging

import uvicorn

from settings import settings

logging.basicConfig(
    level=getattr(logging, settings.service_log_level.upper()),
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

if __name__ == "__main__":
    uvicorn.run(
        "server.app:app",
        host=settings.service_host,
        port=settings.service_port,
        reload=settings.service_reload,
    )
