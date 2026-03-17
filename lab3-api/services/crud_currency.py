from sqlalchemy.orm import Session
from models.models import Currency
from sqlalchemy import select
from typing import Sequence
from get_currencies_from_api import get_currencies_from_api


def get_currencies(session: Session) -> Sequence[Currency]:

    stmt = select(Currency)
    result = session.execute(stmt)

    return result.scalars().all()


def update_currency(session: Session):

    currencies = get_currencies_from_api()

    for currency in currencies:
        new_currency = Currency(
            code=currency["code"], name=currency["name"], value=currency["value"]
        )
