from typing import List, Literal, Optional
from datetime import datetime
from fastapi import HTTPException
from pydantic.class_validators import validator
from app.api.schemas.req_schemas import BaseReq, ListReq


class Payment(BaseReq):
    type: Literal["cash", "cashless"]

    amount: float


class ReceiptCreate(BaseReq):
    products: list[Optional[dict]]
    payment: Payment


class ProductResponse(BaseReq):
    name: str
    price: float
    quantity: float
    total: float


class ReceiptResponse(BaseReq):
    id: int
    products: List[ProductResponse]
    payment: Payment
    total: float
    rest: float
    created_at: datetime


class ReceiptReq(BaseReq):
    id: int


class ReceiptListReq(ListReq):
    created_at_from: Optional[datetime]
    created_at_to: Optional[datetime]
    price_greater: Optional[float]
    price_less: Optional[float]
    payment_type: Optional[str]

    @validator("payment_type", pre=True)
    def validate_payment_type(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            try:
                value in ["cash", "cashless"]
            except Exception as e:  # noqa
                raise HTTPException(status_code=422, detail=f"Invalid value {value}")
        return value
