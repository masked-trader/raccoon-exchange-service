from typing import List, Optional

from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException

from server.models.subscription import (
    ExchangeKlineSubscriptionRequest,
    ExchangeSubscription,
    ExchangeSubscriptionType,
)

router = APIRouter()


@router.get("/")
async def list(x_connection_id: str = Header()) -> List[ExchangeSubscription]:
    return await ExchangeSubscription.find(
        ExchangeSubscription.type == ExchangeSubscriptionType.KLINE,
        ExchangeSubscription.connection == x_connection_id,
    ).to_list()


@router.get("/{symbol:path}/interval/{interval:path}/")
async def retrieve(
    symbol: str,
    interval: str,
    x_connection_id: str = Header(),
) -> Optional[ExchangeSubscription]:
    try:
        return await ExchangeSubscription.find_one(
            ExchangeSubscription.type == ExchangeSubscriptionType.KLINE,
            ExchangeSubscription.symbol == symbol,
            ExchangeSubscription.interval == interval,
            ExchangeSubscription.connection == x_connection_id,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{symbol:path}/")
async def list_symbol(
    symbol: str,
    x_connection_id: str = Header(),
) -> List[ExchangeSubscription]:
    try:
        return await ExchangeSubscription.find(
            ExchangeSubscription.type == ExchangeSubscriptionType.KLINE,
            ExchangeSubscription.symbol == symbol,
            ExchangeSubscription.connection == x_connection_id,
        ).to_list()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
async def create(
    request: ExchangeKlineSubscriptionRequest, x_connection_id: str = Header()
) -> ExchangeSubscription:
    try:
        existing_subscription = await ExchangeSubscription.find_one(
            ExchangeSubscription.type == ExchangeSubscriptionType.KLINE,
            ExchangeSubscription.symbol == request.symbol,
            ExchangeSubscription.interval == request.interval,
            ExchangeSubscription.connection == x_connection_id,
        )

        if existing_subscription:
            return existing_subscription

        subscription = ExchangeSubscription(
            type=ExchangeSubscriptionType.KLINE,
            interval=request.interval,
            connection=x_connection_id,
            symbol=request.symbol,
        )

        return await subscription.create()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/")
async def destroy(
    request: ExchangeKlineSubscriptionRequest, x_connection_id: str = Header()
):
    try:
        item = await ExchangeSubscription.find_one(
            ExchangeSubscription.type == ExchangeSubscriptionType.KLINE,
            ExchangeSubscription.interval == request.interval,
            ExchangeSubscription.connection == x_connection_id,
            ExchangeSubscription.symbol == request.symbol,
        )

        if not item:
            raise HTTPException(status_code=400, detail="subscription not found")

        await ExchangeSubscription.delete(item)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
