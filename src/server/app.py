from fastapi import Depends, FastAPI, Header
from fastapi.exceptions import HTTPException

from server.database import init_db
from server.routes.internal import router as internal_router
from server.routes.order import router as order_router


async def verify_connection_id(x_connection_id=Header()):
    if not x_connection_id:
        raise HTTPException(status_code=400, detail="missing connection ID header")


app = FastAPI(dependencies=[Depends(verify_connection_id)])

app.include_router(
    order_router,
    tags=["exchange", "order"],
    prefix="/api/v1/exchange/order",
)

app.include_router(internal_router, tags=["internal"], prefix="/internal/exchange")


@app.on_event("startup")
async def start_db():
    await init_db()


@app.get("/", tags=["Root"])
async def root() -> dict:
    return {"message": "Raccoon exchange service"}