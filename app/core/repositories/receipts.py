from typing import List

from sqlalchemy import Row, text

from app.core.models.receipt import Receipt
from app.core.repositories.base import BaseSQLAsyncDrivenBaseRepository
from app.extensions.dbs import get_session


class ReceiptRepository(BaseSQLAsyncDrivenBaseRepository):
    MODEL = Receipt

    async def get_receipts_list(self, filter_data: dict) -> List[Row]:
        created_at_from = filter_data.get("created_at_from")
        created_at_to = filter_data.get("created_at_to")
        price_greater = filter_data.get("price_greater")
        price_less = filter_data.get("price_less")
        payment_type = filter_data.get("payment_type")
        limit = filter_data.get("limit")
        offset = filter_data.get("offset")

        q_params = {
            "limit": limit,
            "offset": offset,
        }

        base_stmt = """
            SELECT
                r.id,
                r.user_id,
                r.created_at,
                r.products,
                r.payment_type,
                r.payment_amount,
                r.total,
                r.rest
            FROM receipts as r
        """

        where_stmt = """
            WHERE TRUE
        """

        if created_at_from:
            q_params["created_at_from"] = created_at_from
            where_stmt = f"{where_stmt} AND r.created_at >= :created_at_from"

        if created_at_to:
            q_params["created_at_to"] = created_at_to
            where_stmt = f"{where_stmt} AND r.created_at >= :created_at_to"

        if price_greater:
            q_params["price_greater"] = price_greater
            where_stmt = f"{where_stmt} AND r.total >= :price_greater"

        if price_less:
            q_params["price_less"] = price_less
            where_stmt = f"{where_stmt} AND r.total <= :price_less"

        if payment_type:
            q_params["payment_type"] = payment_type
            where_stmt = f"{where_stmt} AND r.payment_type = :payment_type"

        if not limit:
            stmt = f"{base_stmt} {where_stmt} OFFSET :offset;"
        else:
            q_params["limit_"] = limit
            stmt = f"{base_stmt} {where_stmt} OFFSET :offset LIMIT :limit;"

        async with get_session() as session:
            rows = await session.execute(
                statement=text(stmt),
                params=q_params,
            )

        return list(rows)

    async def get_receipts_list_count(self, filter_data: dict) -> int:
        created_at_from = filter_data.get("created_at_from")
        created_at_to = filter_data.get("created_at_to")
        price_greater = filter_data.get("price_greater")
        price_less = filter_data.get("price_less")
        payment_type = filter_data.get("payment_type")

        q_params = {}

        base_stmt = """
            SELECT
                r.id,
                r.user_id,
                r.created_at,
                r.products,
                r.payment_type,
                r.payment_amount,
                r.total,
                r.rest
            FROM receipts as r

        """

        where_stmt = """
            WHERE TRUE
        """

        if created_at_from:
            q_params["created_at_from"] = created_at_from
            where_stmt = f"{where_stmt} AND r.created_at >= :created_at_from"

        if created_at_to:
            q_params["created_at_to"] = created_at_to
            where_stmt = f"{where_stmt} AND r.created_at <= :created_at_to"

        if price_greater:
            q_params["price_greater"] = price_greater
            where_stmt = f"{where_stmt} AND r.total >= :price_greater"

        if price_less:
            q_params["price_less"] = price_less
            where_stmt = f"{where_stmt} AND r.total <= :price_less"

        if payment_type:
            q_params["payment_type"] = payment_type
            where_stmt = f"{where_stmt} AND r.payment_type = :payment_type"

        stmt = f"{base_stmt} {where_stmt}"

        async with get_session() as session:
            rows = await session.execute(
                statement=text(stmt),
                params=q_params,
            )

        return rows.rowcount
