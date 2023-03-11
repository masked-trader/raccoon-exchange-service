from typing import List, Optional

from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException

from server.models.subscription import ExchangeSubscription, ExchangeSubscriptionType

router = APIRouter()


@router.get("/")
async def list(
    x_connection_id: str = Header(),
) -> List[ExchangeSubscription]:
    return await ExchangeSubscription.find(
        ExchangeSubscription.type == ExchangeSubscriptionType.TICKER,
        ExchangeSubscription.connection == x_connection_id,
    ).to_list()


@router.get("/{symbol}/")
async def retrieve(
    symbol: str,
    x_connection_id: str = Header(),
) -> Optional[ExchangeSubscription]:
    return await ExchangeSubscription.find_one(
        ExchangeSubscription.symbol == symbol,
        ExchangeSubscription.type == ExchangeSubscriptionType.TICKER,
        ExchangeSubscription.connection == x_connection_id,
    )


@router.post("/")
async def create(
    subscription: ExchangeSubscription, x_connection_id: str = Header()
) -> ExchangeSubscription:
    existing_subscription = await ExchangeSubscription.find_one(
        ExchangeSubscription.type == ExchangeSubscriptionType.TICKER,
        ExchangeSubscription.symbol == subscription.symbol,
        ExchangeSubscription.connection == x_connection_id,
    )

    if existing_subscription:
        return existing_subscription

    subscription.type = ExchangeSubscriptionType.TICKER
    subscription.connection = x_connection_id

    return await subscription.create()


@router.delete("/")
async def destroy(subscription: ExchangeSubscription, x_connection_id: str = Header()):
    item = await ExchangeSubscription.find_one(
        ExchangeSubscription.type == ExchangeSubscriptionType.TICKER,
        ExchangeSubscription.symbol == subscription.symbol,
        ExchangeSubscription.connection == x_connection_id,
    )

    if not item:
        raise HTTPException(status_code=400, detail="subscription not found")

    await ExchangeSubscription.delete(item)
