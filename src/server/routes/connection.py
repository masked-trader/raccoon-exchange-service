from typing import List, Optional

import ccxt
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pymongo.errors import DuplicateKeyError

from server.models.connection import ExchangeConnection, ExchangeConnectionView

router = APIRouter()


@router.get("/")
async def list() -> List[ExchangeConnectionView]:
    return await ExchangeConnection.find_all().project(ExchangeConnectionView).to_list()


@router.get("/{id:path}/")
async def retrieve(id: str) -> Optional[ExchangeConnectionView]:
    return await ExchangeConnection.find_one(ExchangeConnection.id == id).project(
        ExchangeConnectionView
    )


@router.post("/")
async def create(connection: ExchangeConnection) -> ExchangeConnection:
    if connection.exchange not in ccxt.exchanges:
        raise HTTPException(status_code=400, detail="invalid exchange name")

    existing_connection = await ExchangeConnection.find_one(
        ExchangeConnection.apiKey == connection.apiKey,
        ExchangeConnection.secret == connection.secret
    )

    if existing_connection:
        raise HTTPException(
            status_code=400,
            detail=f"credentials already configured with connection ID {existing_connection.id}",
        )

    try:
        return await connection.create()

    except DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail=f"connection ID {connection.id} already exists",
        )


@router.delete("/{id:path}/")
async def destroy(id: str):
    connection = await ExchangeConnection.get(id)

    if not connection:
        raise HTTPException(status_code=400, detail="connection ID not found")

    await ExchangeConnection.delete(connection)
