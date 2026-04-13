from fastapi import FastAPI, HTTPException

from receiver.receiver import OrderService
from manager.command_manager import CommandManager

from schemas.schemas import (
    ApplyDiscountRequest,
    CreateOrderRequest,
    ChangeAddressRequest,
    OrderResponse,
)

from commands.apply_discount import ApplyDiscountCommand
from commands.create_order import CreateOrderCommand
from commands.cancel_order import CancelOrderCommand
from commands.confirm_order import ConfirmOrderCommand
from commands.change_address import ChangeAddressCommand


app = FastAPI()
manager = CommandManager()
service = OrderService()


@app.post("/orders", response_model=OrderResponse)
async def create_order(params: CreateOrderRequest):
    return manager.dispatch(
        CreateOrderCommand(
            service,
            params.customer_name,
            params.address,
            params.total_amount,
        )
    )


@app.get("/orders", response_model=list[OrderResponse])
async def get_orders():
    return service.get_all_orders()


@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    try:
        return service.get_order_by_id(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.patch("/orders/{order_id}/confirm", response_model=OrderResponse)
async def confirm_order(order_id: int):
    try:
        return manager.dispatch(ConfirmOrderCommand(service, order_id))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.patch("/orders/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(order_id: int):
    try:
        return manager.dispatch(CancelOrderCommand(service, order_id))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.patch("/orders/{order_id}/apply_discount", response_model=OrderResponse)
async def apply_discount(order_id: int, params: ApplyDiscountRequest):
    try:
        return manager.dispatch(
            ApplyDiscountCommand(service, order_id, params.discount_percent)
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.patch("/orders/{order_id}/change_address", response_model=OrderResponse)
async def change_address(order_id: int, params: ChangeAddressRequest):
    try:
        return manager.dispatch(ChangeAddressCommand(service, order_id, params.address))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get("/commands/history")
async def commands_history():
    return manager.history
