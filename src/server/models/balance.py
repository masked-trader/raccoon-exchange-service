from beanie import Document


class ExchangeBalance(Document):
    connection: str
    asset: str
    free: float
    used: float
    total: float

    class Settings:
        name = "exchange-balance"
