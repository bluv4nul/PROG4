from sqlalchemy.orm import Session
from models.models import User
from sqlalchemy import select
from typing import Sequence


def create_user(session: Session, username: str, email: str) -> User:
    user = User(username=username, email=email)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_users(session: Session) -> Sequence[User]:

    stmt = select(User)
    result = session.execute(stmt)

    return result.scalars().all()


def get_user_by_id(session: Session, user_id: int) -> User | None:

    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)

    return result.scalar_one_or_none()


def delete_user_by_id(session: Session, user_id: int) -> None:
    user = get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise ValueError("Пользователь не найден")

    session.delete(user)
    session.commit()


def update_user_email(session: Session, user_id: int, new_email: str) -> User:
    user = get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise ValueError("Пользователь не найден")

    user.email = new_email
    session.commit()
    return user


def update_user_name(session: Session, user_id: int, new_username: str) -> User:
    user = get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise ValueError("Пользователь не найден")

    user.username = new_username
    session.commit()
    return user
