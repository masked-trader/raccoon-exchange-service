from fastapi import APIRouter, Header

from server.models.balance import ExchangeBalance
from server.models.order import ExchangeOrder

router = APIRouter()


@router.post("/order/")
async def sync_order_data(
    request: ExchangeOrder, x_connection_id=Header()
) -> ExchangeOrder:
    order = await ExchangeOrder.find_one(
        {
            "orderId": request.orderId,
            "symbol": request.symbol,
            "connection": x_connection_id,
        }
    )

    if not order:
        return await request.create()

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


@router.post("/balance/")
async def sync_balance_data(
    request: ExchangeBalance, x_connection_id=Header()
) -> ExchangeBalance:
    balance = await ExchangeBalance.find_one(
        {
            "asset": request.asset,
            "connection": x_connection_id,
        }
    )

    if not balance:
        return await request.create()

    balance.used = request.used
    balance.free = request.free
    balance.total = request.total

    return await balance.save()
