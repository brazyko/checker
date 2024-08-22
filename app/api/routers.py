from fastapi import APIRouter

from app.api.endpoints.auth.auth import router as auth
from app.api.endpoints.receipt.receipts import router as receipt

V1_PREFIX = "api"

api_router = APIRouter(prefix=f"/{V1_PREFIX}")


auth_router = APIRouter(tags=[f"{V1_PREFIX}:auth"])  # noqa
auth_router.include_router(auth)

receipt_router = APIRouter(tags=[f"{V1_PREFIX}:receipt"])  # noqa
receipt_router.include_router(receipt)

common_router = APIRouter(prefix=f"/common", tags=[f"{V1_PREFIX}:common"])  # noqa


api_router.include_router(auth_router)
api_router.include_router(receipt_router)
api_router.include_router(common_router)
