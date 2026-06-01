"""
Пример нарушения и исправления принципа Dependency Inversion (DIP).
"""

from abc import ABC, abstractmethod


# Плохой пример — высокоуровневый модуль привязан к конкретным классам.
class BreadBad:
    def cook(self):
        print("Готовим хлеб (плохой пример)")


class CookieBad:
    def cook(self):
        print("Готовим печенье (плохой пример)")


class KitchenBad:
    def __init__(self):
        self.bread = BreadBad()
        self.cookie = CookieBad()

    def prepare_bread(self):
        self.bread.cook()

    def prepare_cookie(self):
        self.cookie.cook()


def demo_bad():
    print("=== Пример нарушения DIP ===")
    kitchen = KitchenBad()
    kitchen.prepare_bread()
    kitchen.prepare_cookie()


# Хороший пример — Kitchen зависит от абстракции Food, а не от конкретных деталей.
class Food(ABC):
    @abstractmethod
    def cook(self):
        pass


class Bread(Food):
    def cook(self):
        print("Готовим хлеб")


class Cookie(Food):
    def cook(self):
        print("Готовим печенье")


class Kitchen:
    def __init__(self, food: Food):
        self.food = food

    def prepare(self):
        self.food.cook()


def demo_good():
    print("=== Исправленный пример DIP ===")
    kitchen = Kitchen(Bread())
    kitchen.prepare()
    kitchen.food = Cookie()
    kitchen.prepare()


if __name__ == "__main__":
    demo_bad()
    print()
    demo_good()
