from typing import List, Optional

from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException

from client import get_ccxt_client
from server.models.subscription import ExchangeSubscription, ExchangeSubscriptionType

router = APIRouter()


@router.get("/")
async def list(x_connection_id: str = Header()) -> List[ExchangeSubscription]:
    return await ExchangeSubscription.find(
        ExchangeSubscription.type == ExchangeSubscriptionType.KLINE,
        ExchangeSubscription.connection == x_connection_id,
    ).to_list()


@router.get("/{symbol}/")
async def list_symbol(
    symbol: str,
    x_connection_id: str = Header(),
) -> List[ExchangeSubscription]:
    return await ExchangeSubscription.find(
        ExchangeSubscription.type == ExchangeSubscriptionType.KLINE,
        ExchangeSubscription.symbol == symbol,
        ExchangeSubscription.connection == x_connection_id,
    ).to_list()


@router.get("/{symbol}/{interval}/")
async def retrieve(
    symbol: str,
    interval: str,
    x_connection_id: str = Header(),
) -> Optional[ExchangeSubscription]:
    return await ExchangeSubscription.find_one(
        ExchangeSubscription.type == ExchangeSubscriptionType.KLINE,
        ExchangeSubscription.symbol == symbol,
        ExchangeSubscription.interval == interval,
        ExchangeSubscription.connection == x_connection_id,
    )


@router.post("/")
async def create(
    subscription: ExchangeSubscription, x_connection_id: str = Header()
) -> ExchangeSubscription:
    existing_subscription = await ExchangeSubscription.find_one(
        ExchangeSubscription.type == ExchangeSubscriptionType.KLINE,
        ExchangeSubscription.symbol == subscription.symbol,
        ExchangeSubscription.interval == subscription.interval,
        ExchangeSubscription.connection == x_connection_id,
    )

    if existing_subscription:
        return existing_subscription

    client = get_ccxt_client(x_connection_id)

    markets = client.load_markets()
    market_info = markets[subscription.symbol]

    if subscription.interval not in market_info["timeframes"]:
        raise HTTPException(status_code=400, detail="invalid value for interval")

    subscription.type = ExchangeSubscriptionType.KLINE
    subscription.connection = x_connection_id

    return await subscription.create()


@router.delete("/")
async def destroy(subscription: ExchangeSubscription, x_connection_id: str = Header()):
    item = await ExchangeSubscription.find_one(
        ExchangeSubscription.type == ExchangeSubscriptionType.KLINE,
        ExchangeSubscription.symbol == subscription.symbol,
        ExchangeSubscription.interval == subscription.interval,
        ExchangeSubscription.connection == x_connection_id,
    )

    if not item:
        raise HTTPException(status_code=400, detail="subscription not found")

    await ExchangeSubscription.delete(item)