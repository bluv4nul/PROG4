from fastapi import APIRouter, Depends
from db.database import get_session
from schemas.currency_chema import Currency
from services.crud_currency import get_currencies, update_currencies
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.get("/", response_model=list[Currency])
async def get_currencies_endpoint(
    session: AsyncSession = Depends(get_session),
) -> list[Currency]:
    """Получить список всех валют."""

    return await get_currencies(session)


@router.post("/update", response_model=list[Currency])
async def update_currencies_endpoint(
    session: AsyncSession = Depends(get_session),
) -> list[Currency]:
    """Обновить данные о валютах из внешнего API."""

    return await update_currencies(session)
