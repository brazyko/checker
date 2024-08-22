from http.client import HTTPException

from fastapi import APIRouter, Depends
from starlette.responses import PlainTextResponse

from app.api.schemas.receipt import ReceiptCreate, ReceiptListReq, ReceiptReq
from app.core.models.users import User
from app.core.services.auth_service import AuthService
from app.core.services.receipts import ReceiptService
from app.core.utils.receipt_maker import format_receipt_text

router = APIRouter(prefix="/receipts")


@router.post("/create-receipt/", status_code=201)
async def create_receipt(
    user_data: User = Depends(AuthService.validate_user),
    receipt_data: ReceiptCreate = Depends(),
):
    user_id = user_data.id
    receipt_service = ReceiptService()
    receipt = await receipt_service.create_receipt(user_id=user_id, receipt_data=receipt_data)
    return receipt


@router.get("/receipts/", status_code=200)
async def get_receipts(
    user_data: User = Depends(AuthService.validate_user),
    data: ReceiptListReq = Depends(),
):
    raw_data = data.dict(exclude_none=True)
    # filter data pre processing
    filter_data = raw_data
    user_id = user_data.id
    filter_data["user_id"] = user_id
    receipt_service = ReceiptService()
    result = await receipt_service.get_receipts_list(filter_data=filter_data)
    count = await receipt_service.get_receipts_list_count(filter_data=filter_data)
    return {"count": count, "results": result}


@router.get("/receipts/by-id/", status_code=200)
async def get_receipts(
    user_data: User = Depends(AuthService.validate_user),
    data: ReceiptReq = Depends(),
):
    raw_data = data.dict(exclude_none=True)
    # filter data pre processing
    filter_data = raw_data
    user_id = user_data.id
    filter_data["user_id"] = user_id
    receipt_service = ReceiptService()
    result = await receipt_service.get_receipt(filter_data=filter_data)
    return result


@router.get("/{receipt_id}/view/", response_class=PlainTextResponse)
async def view_receipt(receipt_id: int, char_limit: int = 32):
    receipt_service = ReceiptService()
    receipt = await receipt_service.get_first(filter_data={"id": receipt_id})

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    # Format the receipt text
    formatted_receipt = format_receipt_text(receipt, char_limit)
    return formatted_receipt


