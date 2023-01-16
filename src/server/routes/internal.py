from typing import Optional

from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException

from server.models.order import ExchangeOrder

router = APIRouter()


@router.patch("/order/")
async def update(
    request: ExchangeOrder, x_connection_id=Header()
) -> Optional[ExchangeOrder]:
    order = await ExchangeOrder.find_one(
        {
            "orderId": request.orderId,
            "symbol": request.symbol,
            "connection": x_connection_id,
        }
    )

    if not order:
        raise HTTPException(
            status_code=400, detail=f"order {request.symbol} {request.id} not found"
        )

    order.timestamp = request.timestamp
    order.datetime = request.datetime
    order.lastTradeTimestamp = request.lastTradeTimestamp
    order.average = request.average
    order.filled = request.filled
    order.remaining = request.remaining
    order.status = request.status
    order.fee = request.fee
    order.fees = request.fees
    order.trades = request.trades
    order.info = request.info

    return await order.save()
