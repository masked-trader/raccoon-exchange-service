import os

# internal
INTERNAL_CONFIG_API_URL = os.getenv(
    "RACCOON_INTERNAL_CONFIG_API", "http://localhost:8000/internal/config"
)

# service
SERVICE_HOST = os.getenv("RACCOON_EXCHANGE_SERVICE_HOST", "0.0.0.0")
SERVICE_PORT = int(os.getenv("RACCOON_EXCHANGE_SERVICE_PORT", 8000))
SERVICE_RELOAD = bool(os.getenv("RACCOON_EXCHANGE_SERVICE_RELOAD", 1))
SERVICE_LOG_LEVEL = str.upper(os.getenv("RACCOON_EXCHANGE_SERVICE_LOG_LEVEL", "info"))

# mongodb
MONGO_DATABASE = os.getenv("RACCOON_MONGO_DATABASE", "raccoon")
MONGO_CONNECTION_URL = os.getenv(
    "RACCOON_MONGO_CONNECTION_URL", "mongodb://root:rootpassword@mongodb:27017"
)
