from abc import ABC, abstractmethod
from models.order import Order


class Command(ABC):

    @abstractmethod
    def execute(self) -> Order:
        pass

    @abstractmethod
    def describe(self) -> dict:
        pass
