from fastapi import Query
from pydantic import BaseModel

from app.config.settings import settings


class BaseReq(BaseModel):
    pass


class ListReq(BaseReq):
    limit: int = Query(default=settings.BATCH_SIZE, gt=0, description="Limit items")
    offset: int = Query(default=0, ge=0, description="Offset items")
