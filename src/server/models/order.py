from enum import Enum
from typing import Optional

from beanie import Document, Insert, before_event
from pydantic import BaseModel


class OrderSide(Enum):
    buy = "buy"
    sell = "sell"


class OrderType(Enum):
    limit = "limit"
    market = "market"


class ExchangeOrderRequest(BaseModel):
    symbol: str
    type: OrderType
    side: OrderSide
    amount: float
    price: Optional[float]
    params: Optional[dict]

    class Config:
        use_enum_values = True


class ExchangeOrderCancelRequest(BaseModel):
    orderId: str
    symbol: str
    params: Optional[dict]


class ExchangeOrder(Document):
    connection: str
    orderId: str
    symbol: str
    type: str
    side: str
    timestamp: int
    datetime: str
    lastTradeTimestamp: Optional[int]
    amount: float
    price: float
    stopPrice: Optional[float]
    triggerPrice: Optional[float]
    cost: float
    average: Optional[float]
    filled: float
    remaining: float
    status: str
    timeInForce: str
    fee: Optional[dict]
    fees: Optional[list]
    trades: Optional[list]
    postOnly: Optional[bool]
    reduceOnly: Optional[bool]
    clientOrderId: Optional[str]
    info: dict

    @before_event(Insert)
    def update_symbol(self):
        self.symbol = self.symbol.replace("/", "")

    class Settings:
        name = "exchange-order"
