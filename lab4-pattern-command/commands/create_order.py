from commands.base import Command

from receiver.receiver import OrderService
from models.order import Order


class CreateOrderCommand(Command):

    def __init__(
        self,
        service: OrderService,
        customer_name: str,
        address: str,
        total_amount: float,
    ) -> None:
        self._service = service
        self._customer_name = customer_name
        self._address = address
        self._total_amount = total_amount

    def execute(self) -> Order:
        return self._service.create_order(
            self._customer_name, self._address, self._total_amount
        )

    def describe(self) -> dict:
        return {
            "command_name": "CreateOrderCommand",
            "parameters": {
                "customer_name": self._customer_name,
                "address": self._address,
                "total_amount": self._total_amount,
            },
        }
