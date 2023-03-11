from typing import List, Optional

from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException

from server.models.subscription import (
    ExchangeSubscription,
    ExchangeSubscriptionType,
    ExchangeTickerSubscriptionRequest,
)

router = APIRouter()


@router.get("/")
async def list(
    x_connection_id: str = Header(),
) -> List[ExchangeSubscription]:
    try:
        return await ExchangeSubscription.find(
            ExchangeSubscription.type == ExchangeSubscriptionType.TICKER,
            ExchangeSubscription.connection == x_connection_id,
        ).to_list()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{symbol:path}/")
async def retrieve(
    symbol: str,
    x_connection_id: str = Header(),
) -> Optional[ExchangeSubscription]:
    try:
        return await ExchangeSubscription.find_one(
            ExchangeSubscription.symbol == symbol,
            ExchangeSubscription.type == ExchangeSubscriptionType.TICKER,
            ExchangeSubscription.connection == x_connection_id,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
async def create(
    request: ExchangeTickerSubscriptionRequest, x_connection_id: str = Header()
) -> ExchangeSubscription:
    try:
        existing_subscription = await ExchangeSubscription.find_one(
            ExchangeSubscription.type == ExchangeSubscriptionType.TICKER,
            ExchangeSubscription.symbol == request.symbol,
            ExchangeSubscription.connection == x_connection_id,
        )

        if existing_subscription:
            return existing_subscription

        subscription = ExchangeSubscription(
            type=ExchangeSubscriptionType.TICKER,
            connection=x_connection_id,
            symbol=request.symbol,
            interval=None,
        )

        return await subscription.create()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/")
async def destroy(
    request: ExchangeTickerSubscriptionRequest, x_connection_id: str = Header()
):
    try:
        item = await ExchangeSubscription.find_one(
            ExchangeSubscription.type == ExchangeSubscriptionType.TICKER,
            ExchangeSubscription.symbol == request.symbol,
            ExchangeSubscription.connection == x_connection_id,
        )

        if not item:
            raise HTTPException(status_code=400, detail="subscription not found")

        await ExchangeSubscription.delete(item)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
