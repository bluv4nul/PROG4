from models.order import Order, OrderStatus

Orders = {}


class OrderService:
    @staticmethod
    def get_all_orders() -> list[Order]:
        if not Orders:
            return []
        return list(Orders.values())

    @staticmethod
    def get_order_by_id(order_id: int) -> Order:
        if order_id not in Orders:
            raise ValueError("ORDER NOT FOUND!")
        return Orders[order_id]

    @staticmethod
    def create_order(
        customer_name: str,
        address: str,
        total_amount: float,
    ) -> Order:
        order_id = max(Orders.keys(), default=0) + 1
        order = Order(
            order_id=order_id,
            customer_name=customer_name,
            address=address,
            total_amount=total_amount,
        )
        Orders[order.order_id] = order
        return order

    @staticmethod
    def change_order_address(order_id: int, address: str) -> Order:
        order = OrderService.get_order_by_id(order_id)
        if (
            order.status == OrderStatus.CANCELLED
            or order.status == OrderStatus.CONFIRMED
        ):
            raise ValueError("ORDER CANNOT BE CHANGED!")
        order.address = address
        return order

    @staticmethod
    def apply_discount(order_id: int, discount_percent: float) -> Order:
        order = OrderService.get_order_by_id(order_id)
        if (
            order.status == OrderStatus.CANCELLED
            or order.status == OrderStatus.CONFIRMED
        ):
            raise ValueError("ORDER CANNOT BE CHANGED!")
        order.discount_percent = discount_percent
        return order

    @staticmethod
    def confirm_order(order_id: int) -> Order:
        order = OrderService.get_order_by_id(order_id)
        if order.status == OrderStatus.CANCELLED:
            raise ValueError("ORDER CANNOT BE CHANGED!")
        if order.status == OrderStatus.CONFIRMED:
            raise ValueError("ORDER ALREADY CONFIRMED!")
        order.status = OrderStatus.CONFIRMED
        return order

    @staticmethod
    def cancel_order(order_id: int) -> Order:
        order = OrderService.get_order_by_id(order_id)
        if order.status == OrderStatus.CANCELLED:
            raise ValueError("ALREADY CANCELLED!")
        order.status = OrderStatus.CANCELLED
        return order
