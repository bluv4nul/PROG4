from commands.base import Command

from receiver.receiver import OrderService
from models.order import Order


class ConfirmOrderCommand(Command):

    def __init__(self, service: OrderService, order_id: int) -> None:
        self._service = service
        self._order_id = order_id

    def execute(self) -> Order:
        return self._service.confirm_order(self._order_id)

    def describe(self) -> dict:
        return {
            "command_name": "ConfirmOrderCommand",
            "parameters": {
                "order_id": self._order_id,
            },
        }
