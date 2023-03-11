from typing import List, Optional

from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException

from client import get_ccxt_client
from server.models.order import (
    ExchangeOrder,
    ExchangeOrderCancelRequest,
    ExchangeOrderRequest,
)

router = APIRouter()


@router.get("/{symbol}/")
async def list(symbol: str, x_connection_id: str = Header()) -> List[ExchangeOrder]:
    return await ExchangeOrder.find(
        ExchangeOrder.symbol == symbol, ExchangeOrder.connection == x_connection_id
    ).to_list()


@router.get("/{symbol}/{order_id}/")
async def retrieve(
    symbol: str, order_id: str, x_connection_id: str = Header()
) -> Optional[ExchangeOrder]:
    return await ExchangeOrder.find_one(
        ExchangeOrder.symbol == symbol,
        ExchangeOrder.orderId == order_id,
        ExchangeOrder.connection == x_connection_id,
    )


@router.post("/")
async def create(
    request: ExchangeOrderRequest, x_connection_id: str = Header()
) -> ExchangeOrder:
    client = get_ccxt_client(x_connection_id)

    try:
        response = client.create_order(
            symbol=request.symbol,
            type=request.type,
            side=request.side,
            amount=request.amount,
            price=request.price,
            params=request.params,
        )

        order_data = {
            **response,
            "connection": x_connection_id,
            "orderId": response["id"],
        }

        del order_data["id"]

        order_item = ExchangeOrder(**order_data)
        await order_item.create()

        return order_item

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{symbol}/sync/")
async def sync_orders(symbol: str, x_connection_id: str = Header()):
    client = get_ccxt_client(x_connection_id)

    for item in client.fetch_orders(symbol):  # type: ignore
        order_data = {**item, "connection": x_connection_id, "orderId": item["id"]}

        del order_data["id"]

        order = await ExchangeOrder.find_one(
            ExchangeOrder.connection == x_connection_id,
            ExchangeOrder.orderId == order_data["orderId"],
            ExchangeOrder.symbol == symbol,
        )

        if not order:
            order_item = ExchangeOrder(**order_data)
            await order_item.create()

        else:
            order.timestamp = order_data["timestamp"]
            order.datetime = order_data["datetime"]
            order.lastTradeTimestamp = order_data["lastTradeTimestamp"]
            order.average = order_data["average"]
            order.filled = order_data["filled"]
            order.remaining = order_data["remaining"]
            order.status = order_data["status"]
            order.fee = order_data["fee"]
            order.fees = order_data["fees"]
            order.trades = order_data["trades"]
            order.info = order_data["info"]

            await order.save()


@router.post("/cancel/")
async def cancel(request: ExchangeOrderCancelRequest, x_connection_id: str = Header()):
    client = get_ccxt_client(x_connection_id)

    try:
        return client.cancel_order(
            id=request.orderId, symbol=request.symbol, params=request.params
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
