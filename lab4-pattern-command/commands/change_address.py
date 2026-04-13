from commands.base import Command

from receiver.receiver import OrderService
from models.order import Order


class ChangeAddressCommand(Command):

    def __init__(self, service: OrderService, order_id: int, address: str) -> None:
        self._service = service
        self._order_id = order_id
        self._address = address

    def execute(self) -> Order:
        return self._service.change_order_address(self._order_id, self._address)

    def describe(self) -> dict:
        return {
            "command_name": "ChangeAddressCommand",
            "parameters": {
                "order_id": self._order_id,
                "address": self._address,
            },
        }
