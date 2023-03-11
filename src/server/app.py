from fastapi import Depends, FastAPI, Header
from fastapi.exceptions import HTTPException

from server.database import init_db, init_redis
from server.routes.balance import router as balance_router
from server.routes.connection import router as connection_router
from server.routes.internal import router as internal_router
from server.routes.market import router as market_router
from server.routes.order import router as order_router
from server.routes.subscription.kline import router as kline_sub_router
from server.routes.subscription.ticker import router as ticker_sub_router


async def verify_connection_id(x_connection_id=Header()):
    if not x_connection_id:
        raise HTTPException(status_code=400, detail="missing connection ID header")


app = FastAPI()

app.include_router(
    connection_router,
    tags=["exchange", "connection"],
    prefix="/api/v1/exchange/connection",
)

app.include_router(
    balance_router,
    tags=["exchange", "balance"],
    prefix="/api/v1/exchange/balance",
    dependencies=[Depends(verify_connection_id)],
)

app.include_router(
    order_router,
    tags=["exchange", "order"],
    prefix="/api/v1/exchange/order",
    dependencies=[Depends(verify_connection_id)],
)

app.include_router(
    kline_sub_router,
    tags=["exchange", "subscription", "ticker"],
    prefix="/api/v1/exchange/subscription/kline",
    dependencies=[Depends(verify_connection_id)],
)

app.include_router(
    ticker_sub_router,
    tags=["exchange", "subscription", "ticker"],
    prefix="/api/v1/exchange/subscription/ticker",
    dependencies=[Depends(verify_connection_id)],
)

app.include_router(
    market_router,
    tags=["exchange", "market"],
    prefix="/api/v1/exchange/market",
    dependencies=[Depends(verify_connection_id)],
)

app.include_router(
    internal_router,
    tags=["internal"],
    prefix="/internal/exchange",
    dependencies=[Depends(verify_connection_id)],
)


@app.on_event("startup")
async def start_db():
    await init_db()
    await init_redis()


@app.get("/", tags=["Root"])
async def root() -> dict:
    return {"message": "Raccoon exchange service"}
