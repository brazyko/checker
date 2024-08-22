from app.core.dto.base import BaseDTO


class ProductDTO(BaseDTO):
    name: str
    price: float
    quantity: float
    total: float
