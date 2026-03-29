"""CRUD-операции для модели Subscription."""

from sqlalchemy import select
from typing import Optional

from models.models import Subscription
from sqlalchemy.ext.asyncio import AsyncSession


async def create_subscription(
    session: AsyncSession, user_id: int, currency_id: int
) -> Subscription:
    """Создает новую подписку пользователя на валюту.

    Args:
        user_id: ID пользователя, который подписывается.
        currency_id: ID валюты, на которую подписываются.

    Returns:
        Созданный объект Subscription.
    """

    subscription = Subscription(user_id=user_id, currency_id=currency_id)

    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)

    return subscription


async def delete_subscription(
    session: AsyncSession, user_id: int, currency_id: int
) -> None:
    """Удаляет подписку пользователя на указанную валюту.

    Args:
        user_id: ID пользователя, чью подписку удаляют.
        currency_id: ID валюты, подписку на которую удаляют.

    Raises:
        ValueError: Если подписка не найдена.
    """

    stmt = select(Subscription).where(
        Subscription.user_id == user_id,
        Subscription.currency_id == currency_id,
    )
    result = await session.execute(stmt)
    subscription: Optional[Subscription] = result.scalar_one_or_none()

    if subscription is None:
        raise ValueError("Подписка не найдена")

    session.delete(subscription)
    await session.commit()
