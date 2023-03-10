from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException

from client import get_ccxt_client

router = APIRouter()


@router.get("/info/")
async def list_market(x_connection_id: str = Header()):
    try:
        client = get_ccxt_client(x_connection_id)
        return client.load_markets()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/info/{symbol}/")
async def retrieve_market(symbol: str, x_connection_id: str = Header()):
    try:
        markets = await list_market(x_connection_id=x_connection_id)
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


@router.get("/ticker/{symbol}/")
async def retrieve_ticker(symbol: str, x_connection_id: str = Header()):
    try:
        client = get_ccxt_client(x_connection_id)
        return client.fetch_ticker(symbol=symbol)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/kline/{symbol}/{interval}/")
async def retrieve_kline(symbol: str, interval: str, x_connection_id: str = Header()):
    try:
        client = get_ccxt_client(x_connection_id)
        return client.fetch_ohlcv(symbol=symbol, timeframe=interval)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
