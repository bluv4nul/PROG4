from abc import ABC, abstractmethod
from sqlite3 import Date


class Reader:
    # Заглушка
    pass


class Book:
    # Заглушка
    pass


class Command(ABC):
    """
    Интерфейс команлы
    """

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class LibraryService:
    """Receiver. Получатель: бизнес логика"""

    def give_book(self, reader: Reader, book: Book, due_date: Date) -> None:
        pass

    def take_book_back(self, book: Book) -> None:
        # Представим что все книги разные, так проще.
        pass

    def extend_book(self, book: Book, new_due_date: Date) -> None:
        pass


class TakeBookCommand(Command):

    def __init__(
        self, library: LibraryService, reader: Reader, book: Book, due_date: Date
    ) -> None:
        self._library = library
        self._reader = reader
        self._book = book
        self._due_date = due_date

    def execute(self) -> None:
        # Логика взятия книги из библиотеки. Взаимодействие с БД будет в отдельном файле.
        pass

    def undo(self) -> None:
        # Отмена взятия книги
        pass


class ReturnBookCommand(Command):

    def __init__(self, library: LibraryService, book: Book) -> None:
        self._library = library
        self._book = book

    def execute(self) -> None:
        # Логика возврата книги в библиотеку. Взаимодействие с БД будет в отдельном файле.
        pass

    def undo(self) -> None:
        # Отмена
        pass


class ExtendBook(Command):

    def __init__(
        self, library: LibraryService, reader: Reader, book: Book, new_due_date: Date
    ) -> None:
        self._library = library
        self._reader = reader
        self._book = book
        self._new_due_date = new_due_date

    def execute(self) -> None:
        # Логика продления книги из библитеки. Взаимодействие с БД будет в отдельном файле.
        pass

    def undo(self) -> None:
        # Логика отмены
        pass


class LibraryTerminal:
    """Инициатор: запускает команды и хранит историю"""

    def __init__(self) -> None:
        self._history: list[Command] = []

    def submit(self, command: Command) -> None:
        # Выполнение команды
        pass

    def undo_last(self) -> None:
        # Отмена последней команды
        pass


if __name__ == "__main__":
    library = LibraryService()
    # ...
