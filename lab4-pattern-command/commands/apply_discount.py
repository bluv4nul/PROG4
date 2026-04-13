from commands.base import Command

from receiver.receiver import OrderService
from models.order import Order


class ApplyDiscountCommand(Command):

    def __init__(
        self, service: OrderService, order_id: int, discount_percent: float
    ) -> None:
        self._service = service
        self._order_id = order_id
        self._discount_percent = discount_percent

    def execute(self) -> Order:
        return self._service.apply_discount(self._order_id, self._discount_percent)

    def describe(self) -> dict:
        return {
            "command_name": "ApplyDiscountCommand",
            "parameters": {
                "order_id": self._order_id,
                "discount_percent": self._discount_percent,
            },
        }
