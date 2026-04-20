from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.order import Order, OrderItem
from api.schemas.order_in import OrderCreateCommand
from infrastructure.db.models import OrderModel, OrderItemModel, OutboxModel
import uuid

class CreateOrderUseCase:
    async def execute(self, cmd: OrderCreateCommand, db: AsyncSession):
        items = [OrderItem(**item.model_dump()) for item in cmd.items]
        
        order = Order.create(
            user_id=cmd.user_id,
            items=items,
            shipping_address=cmd.shipping_address
        )
        
        order_model = OrderModel(
            id=uuid.UUID(order.id),
            user_id=uuid.UUID(order.user_id),
            status=order.status.value,
            total_amount=order.total_amount,
            currency=order.currency,
            shipping_address=order.shipping_address,
            items=[OrderItemModel(
                id=uuid.UUID(i.id),
                product_id=uuid.UUID(i.product_id),
                product_name=i.product_name,
                product_sku=i.sku,
                unit_price=i.unit_price,
                quantity=i.quantity,
                subtotal=i.subtotal
            ) for i in items]
        )
        
        outbox_event = OutboxModel(
            aggregate_id=uuid.UUID(order.id),
            aggregate_type='Order',
            event_type='order.order.created',
            payload=order.to_event_dict()
        )

        async with db.begin():
            db.add(order_model)
            db.add(outbox_event)
            
        return order
