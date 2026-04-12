from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class Reader(Base):
    """
    Структура таблицы Readerx
    """

    __tablename__ = "Reader"

    # Столбцы
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    # Связь
    rents: Mapped[list["Rent"]] = relationship(back_populates="reader")

    def __init__(self, name: str, email: str):
        pass


class Book(Base):
    """
    Структура таблицы Book
    """

    __tablename__ = "Book"

    # Столбцы
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)

    # Связь
    rents: Mapped[list["Rent"]] = relationship(back_populates="book")

    def __init__(self, name: str, author: str, amount: int):
        pass


class Rent(Base):
    """
    Структура таблицы Rent
    """

    # Столбцы
    id: Mapped[int] = mapped_column(primary_key=True)
    reader_id: Mapped[int] = mapped_column(ForeignKey("Reader.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("Book.id"), nullable=False)
    due_date: Mapped[datetime] = mapped_column(nullable=False)

    # Связи
    book: Mapped["Book"] = relationship(back_populates="rents")
    reader: Mapped["Reader"] = relationship(back_populates="rents")
