from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException

from client import get_ccxt_client

router = APIRouter()


@router.get("/info/")
async def list_markets(x_connection_id: str = Header()):
    try:
        client = get_ccxt_client(x_connection_id)
        return client.load_markets()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/info/{symbol:path}/")
async def retrieve_markets(symbol: str, x_connection_id: str = Header()):
    try:
        markets = await list_markets(x_connection_id)

        if symbol not in markets:
            raise HTTPException(status_code=400, detail=f"symbol {symbol} not found")

        return markets[symbol]

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/info/sync/")
async def sync_markets(x_connection_id: str = Header()):
    try:
        client = get_ccxt_client(x_connection_id)
        return client.load_markets(reload=True)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/ticker/")
async def list_ticker(x_connection_id: str = Header()):
    try:
        client = get_ccxt_client(x_connection_id)
        return client.fetch_tickers()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/ticker/{symbol:path}/")
async def retrieve_ticker(symbol: str, x_connection_id: str = Header()):
    try:
        client = get_ccxt_client(x_connection_id)
        return client.fetch_ticker(symbol=symbol)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/kline/{symbol:path}/interval/{interval:path}/")
async def retrieve_kline(symbol: str, interval: str, x_connection_id: str = Header()):
    try:
        client = get_ccxt_client(x_connection_id)
        client_properties = client.describe()

        if interval not in client_properties["timeframes"]:
            raise HTTPException(status_code=400, detail="invalid value for interval")

        return client.fetch_ohlcv(symbol=symbol, timeframe=interval)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
