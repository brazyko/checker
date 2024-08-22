from datetime import datetime
from typing import Optional, List

from app.core.dto.product import ProductDTO
from app.core.dto.receipt import ReceiptDTO, PaymentDTO
from app.core.models.receipt import Receipt
from app.core.repositories.receipts import ReceiptRepository
from app.core.services.base import BaseEntityService


class ReceiptService(BaseEntityService):
    def __init__(self) -> None:
        self.repository = ReceiptRepository()

    async def count(self, filter_data: Optional[dict] = None) -> int:
        if not filter_data:
            filter_data = {}
        count = await self.repository.count(filter_data=filter_data)
        return count

    async def get_first(self, filter_data: Optional[dict] = None) -> Optional[Receipt]:
        if not filter_data:
            filter_data = {}
        result = await self.repository.get_first(filter_data=filter_data)
        return result

    async def create_receipt(self, user_id: int, receipt_data):
        receipt_repository = ReceiptRepository()
        products_raw = []
        for product in receipt_data.products:
            total = product["price"] * product["quantity"]
            product_raw = {
                "name": product["name"],
                "price": product["price"],
                "quantity": product["quantity"],
                "total": total
            }
            products_raw.append(product_raw)

        total_price = round(sum(product["total"] for product in products_raw), 2)
        rest = round(receipt_data.payment.amount - total_price, 2)
        amount = round(receipt_data.payment.amount, 2)
        receipt_raw = {
            "user_id": user_id,
            "created_at": datetime.now(),
            "products": products_raw,
            "payment_type": receipt_data.payment.type,
            "payment_amount": amount,
            "total": total_price,
            "rest": rest
        }
        await receipt_repository.create(data=receipt_raw)
        receipt = await receipt_repository.get_first(filter_data=receipt_raw)
        products = []
        for product in receipt.products:
            product_d = ProductDTO(
                name=product["name"],
                price=product["price"],
                quantity=product["quantity"],
                total=product["total"]
            )
            products.append(product_d)
        payment = PaymentDTO(
            type=receipt.payment_type,
            amount=receipt.payment_amount,
        )
        receipt = ReceiptDTO(
            id=receipt.id,
            products=products,
            payment=payment,
            total=receipt.total,
            rest=receipt.rest,
            created_at=receipt.created_at
        )
        return receipt

    async def get_receipt(self, filter_data: dict):
        receipt_id = filter_data.get("id")
        receipt = await self.repository.get_first(filter_data={"id": receipt_id})
        products = []
        for product in receipt.products:
            product_d = ProductDTO(
                name=product["name"],
                price=product["price"],
                quantity=product["quantity"],
                total=product["total"]
            )
            products.append(product_d)
        payment = PaymentDTO(
            type=receipt.payment_type,
            amount=receipt.payment_amount,
        )
        receipt = ReceiptDTO(
            id=receipt.id,
            products=products,
            payment=payment,
            total=receipt.total,
            rest=receipt.rest,
            created_at=receipt.created_at
        )
        return receipt

    async def get_receipts_list(self, filter_data: dict) -> List[Receipt]:
        results = await self.repository.get_receipts_list(filter_data=filter_data)
        receipts = []
        for receipt in results:
            products = []
            for product in receipt.products:
                product_d = ProductDTO(
                    name=product["name"],
                    price=product["price"],
                    quantity=product["quantity"],
                    total=product["total"]
                )
                products.append(product_d)
            payment = PaymentDTO(
                type=receipt.payment_type,
                amount=receipt.payment_amount,
            )
            receipt = ReceiptDTO(
                id=receipt.id,
                products=products,
                payment=payment,
                total=receipt.total,
                rest=receipt.rest,
                created_at=receipt.created_at
            )
            receipts.append(receipt)
        return receipts

    async def get_receipts_list_count(self, filter_data: dict) -> int:
        count = await self.repository.get_receipts_list_count(filter_data=filter_data)
        return count

