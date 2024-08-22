from datetime import datetime
from typing import List, Optional, Literal

from app.core.dto.base import BaseDTO
from app.core.dto.product import ProductDTO


class PaymentDTO(BaseDTO):
    type: Literal["cash", "cashless"]
    amount: float


class ReceiptDTO(BaseDTO):
    id: int
    products: List[ProductDTO]
    payment: PaymentDTO
    total: Optional[float]
    rest: Optional[float]
    created_at: Optional[datetime]
