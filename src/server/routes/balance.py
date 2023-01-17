from typing import List, Optional

from fastapi import APIRouter, Header

from server.models.balance import ExchangeBalance
from util import get_exchange_client

router = APIRouter()


@router.get("/")
async def list(x_connection_id: str = Header()) -> List[ExchangeBalance]:
    return await ExchangeBalance.find({"connection": x_connection_id}).to_list()


@router.get("/{name}/")
async def retrieve(
    name: str, x_connection_id: str = Header()
) -> Optional[ExchangeBalance]:
    return await ExchangeBalance.find_one(
        {"connection": x_connection_id, "asset": name}
    )


@router.post("/sync/")
async def sync_balances(x_connection_id: str = Header()):
    client = get_exchange_client(x_connection_id)

    resp = client.fetch_balance()

    for name in resp["total"]:
        balance = await ExchangeBalance.find_one(
            {"connection": x_connection_id, "asset": name}
        )

        balance_data = resp[name]

        if not balance:
            balance_item = ExchangeBalance(
                asset=name, connection=x_connection_id, **balance_data
            )

            await balance_item.create()

        else:
            balance.free = balance_data["free"]
            balance.used = balance_data["used"]
            balance.total = balance_data["total"]

            await balance.save()
