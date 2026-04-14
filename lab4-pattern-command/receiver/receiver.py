from models.order import Order, OrderStatus


class OrderService:
    def __init__(self):
        self._orders = {}

    def get_all_orders(self) -> list[Order]:
        if not self._orders:
            return []
        return list(self._orders.values())

    def get_order_by_id(self, order_id: int) -> Order:
        if order_id not in self._orders:
            raise ValueError("ORDER NOT FOUND!")
        return self._orders[order_id]

    def create_order(
        self,
        customer_name: str,
        address: str,
        total_amount: float,
    ) -> Order:
        order_id = max(self._orders.keys(), default=0) + 1
        order = Order(
            order_id=order_id,
            customer_name=customer_name,
            address=address,
            total_amount=total_amount,
        )
        self._orders[order.order_id] = order
        return order

    def change_order_address(self, order_id: int, address: str) -> Order:
        order = self.get_order_by_id(order_id)
        if (
            order.status == OrderStatus.CANCELLED
            or order.status == OrderStatus.CONFIRMED
        ):
            raise ValueError("ORDER CANNOT BE CHANGED!")
        order.address = address
        return order

    def apply_discount(self, order_id: int, discount_percent: float) -> Order:
        order = self.get_order_by_id(order_id)
        if (
            order.status == OrderStatus.CANCELLED
            or order.status == OrderStatus.CONFIRMED
        ):
            raise ValueError("ORDER CANNOT BE CHANGED!")
        order.discount_percent = discount_percent
        return order

    def confirm_order(self, order_id: int) -> Order:
        order = self.get_order_by_id(order_id)
        if order.status == OrderStatus.CANCELLED:
            raise ValueError("ORDER CANNOT BE CHANGED!")
        if order.status == OrderStatus.CONFIRMED:
            raise ValueError("ORDER ALREADY CONFIRMED!")
        order.status = OrderStatus.CONFIRMED
        return order

    def cancel_order(self, order_id: int) -> Order:
        order = self.get_order_by_id(order_id)
        if order.status == OrderStatus.CANCELLED:
            raise ValueError("ALREADY CANCELLED!")
        order.status = OrderStatus.CANCELLED
        return order
