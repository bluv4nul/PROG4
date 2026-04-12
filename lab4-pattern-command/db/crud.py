from models.models import Reader, Book, Rent

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


## Reader ##


async def add_reader(session: AsyncSession, name: str, email: str) -> Reader:
    """Создает нового читателя"""

    reader = Reader(name, email)

    session.add(reader)

    await session.commit()
    await session.refresh(reader)

    return reader


async def get_readers(session: AsyncSession):
    """Возвращает всех читателей"""

    stmt = select(Reader)
    result = await session.execute(stmt)

    return result.scalars().all()


## Book ##


async def add_book(session: AsyncSession, name: str, author: str, amount: str) -> Book:
    """Создает нового читателя"""

    book = Book(name, author, amount)

    await session.commit()
    await session.refresh(book)

    return book


async def get_books(session: AsyncSession):
    """Возвращает все книги"""

    stmt = select(Book)
    result = await session.execute(stmt)

    return result.scalars().all()

async def take_book(session: AsyncSession, book: Book) -> None:
    # Имитируем взятие книги, количество взятой книги уменьшается на единицу.


## Rent ##


async def rent_book(
    session: AsyncSession, reader_id: int, book_name: str, book_author: str
):

    book = ( await session.execute(
        select(Book).where(Book.name == book_name and Book.author == book_author)
    )).scalar_one_or_none()

    user = (await session.execute(select(Reader).where(Reader.id == reader_id))).scalar_one_or_none()

    rent = Rent(reader_id=reader_id, book_id=book.id) 
