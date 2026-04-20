from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from api.schemas.order_in import OrderCreateCommand
from application.create_order import CreateOrderUseCase

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    cmd: OrderCreateCommand,
    db: AsyncSession = Depends(get_db)
):
    use_case = CreateOrderUseCase()
    order = await use_case.execute(cmd, db)
    return order.to_event_dict()
