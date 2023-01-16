from typing import List, Optional

from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException

from server.models.order import (
    ExchangeOrder,
    ExchangeOrderCancelRequest,
    ExchangeOrderRequest,
)
from util import get_exchange_client

router = APIRouter()


@router.get("/{symbol}/")
async def list(symbol: str, x_connection_id: str = Header()) -> List[ExchangeOrder]:
    return await ExchangeOrder.find(
        {"symbol": symbol, "connection": x_connection_id}
    ).to_list()


@router.get("/{symbol}/{order_id}/")
async def retrieve(
    symbol: str, order_id: str, x_connection_id: str = Header()
) -> Optional[ExchangeOrder]:
    return await ExchangeOrder.find_one(
        {"symbol": symbol, "orderId": order_id, "connection": x_connection_id}
    )


@router.post("/")
async def create(
    request: ExchangeOrderRequest, x_connection_id: str = Header()
) -> ExchangeOrder:
    client = get_exchange_client(x_connection_id)

    try:
        return client.create_order(
            symbol=request.symbol,
            type=request.type,
            side=request.side,
            amount=request.amount,
            price=request.price,
            params=request.params,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/cancel/")
async def cancel(request: ExchangeOrderCancelRequest, x_connection_id: str = Header()):
    client = get_exchange_client(x_connection_id)

    try:
        return client.cancel_order(
            id=request.orderId, symbol=request.symbol, params=request.params
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
