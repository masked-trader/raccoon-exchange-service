from pydantic import AnyHttpUrl, BaseSettings, MongoDsn


class Settings(BaseSettings):
    internal_ssl_verify: bool = False
    internal_api_base_url: AnyHttpUrl = "http://localhost:5284"  # type: ignore

    mongo_database: str = "raccoon"
    mongo_connection_url: MongoDsn = "mongodb://localhost:27017"  # type: ignore

    service_host: str = "0.0.0.0"
    service_port: int = 8000
    service_reload: bool = True
    service_log_level: str = "info"

    class Config:
        env_prefix = "raccoon_"


settings = Settings()
