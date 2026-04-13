from enum import Enum


class OrderStatus(Enum):
    NEW = "NEW"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class Order:
    def __init__(
        self,
        order_id: int,
        customer_name: str,
        address: str,
        total_amount: float,
        discount_percent: float = 0,
        status: OrderStatus = OrderStatus.NEW,
    ):
        if type(status) != OrderStatus:
            raise ValueError("WRONG STATUS! MUST BE OrderStatus!")
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("WRONG DISCOUNT! MUST BE PERCENT!")
        if total_amount <= 0:
            raise ValueError("WRONG AMOUNT! MUST BE > 0!")
        if customer_name == "" or customer_name == " ":
            raise ValueError("WRONG NAME! MUST BE NOT EMPTY!")
        if address == "" or address == " ":
            raise ValueError("WRONG ADDRESS! MUST BE NOT EMPTY!")

        self._order_id = order_id
        self._customer_name = customer_name
        self._address = address
        self._status = status
        self._total_amount = total_amount
        self._discount_percent = discount_percent

    @property
    def order_id(self):
        return self._order_id

    @property
    def customer_name(self):
        return self._customer_name

    @customer_name.setter
    def customer_name(self, value: str):
        if value == "" or value == " ":
            raise ValueError("WRONG NAME! MUST BE NOT EMPTY!")
        self._customer_name = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value: str):
        if value == "" or value == " ":
            raise ValueError("WRONG ADDRESS! MUST BE NOT EMPTY!")
        self._address = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: OrderStatus):
        if type(value) != OrderStatus:
            raise ValueError("WRONG STATUS! MUST BE OrderStatus!")
        self._status = value

    @property
    def total_amount(self):
        return self._total_amount

    @total_amount.setter
    def total_amount(self, value: float):
        if value <= 0:
            raise ValueError("WRONG AMOUNT! MUST BE > 0!")
        self._total_amount = value

    @property
    def discount_percent(self):
        return self._discount_percent

    @discount_percent.setter
    def discount_percent(self, value: float):
        if value < 0 or value > 100:
            raise ValueError("WRONG DISCOUNT! MUST BE PERCENT!")
        self._discount_percent = value

    @property
    def final_amount(self):
        return self._total_amount * (1 - self._discount_percent / 100)
