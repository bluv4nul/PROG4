from pydantic import BaseModel
from models.order import OrderStatus


class CreateOrderRequest(BaseModel):

    customer_name: str
    address: str
    total_amount: float


class ApplyDiscountRequest(BaseModel):

    discount_percent: float


class ChangeAddressRequest(BaseModel):

    address: str


class OrderResponse(BaseModel):

    order_id: int
    customer_name: str
    address: str
    total_amount: float
    status: OrderStatus
    discount_percent: float = 0
