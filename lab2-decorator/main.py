import requests
import json
import csv


class Currencies:
    """
    class Сomponent():

    Базовое поведение программы.
    """

    def __init__(self) -> None:
        self.currencies = None
        self.date = None
        pass

    def getCurrencies(self) -> dict:
        pass

    def createFile(self) -> None:
        pass


class GetCurrencies(Currencies):
    """
    class concreteComponent(Component):

    Класс возвращающий dict (json)
    А так же создающий соответствующий файл

    Принимает класс Currencies
    """

    def getCurrencies(self, url="https://www.cbr-xml-daily.ru/daily_json.js") -> dict:

        response = requests.get(url)
        response.raise_for_status()

        self.currencies = response.json()

        if "Valute" not in self.currencies:
            raise KeyError(
                "Данные повреждены или получены неправильно, отсутвует информация о валютах"
            )
        else:
            self.date = self.currencies["Date"]
            self.currencies = self.currencies["Valute"]
            return self.currencies

    def createFile(self) -> None:
        if self.currencies is None:
            raise ValueError("Переменная не имеет данных о валютах")
        else:
            with open("./files/result_in_json.json", "w", encoding="utf-8") as file:
                json.dump(self.currencies, file, ensure_ascii=False)


class Convert(Currencies):
    """
    class Decorator():

    Декоратор, описывающий общее поведение декораторов
    """

    _currencies: Currencies = None

    def __init__(self, currencies: Currencies) -> None:
        self._currencies = currencies

    @property
    def currencies(self) -> Currencies:
        return self._currencies

    def convert(self) -> dict:
        pass

    def createFile(self) -> None:
        pass


class ConvertToCSV(Convert):
    """
    class ConcreteDecoratorA():

    Декоратор переводящий JSON формат в CSV формат
    """

    def __init__(self, currencies):
        self.csv_data = []

    def convert(self) -> dict:

        data = self._currencies.getCurrencies()

        if data:
            first_currency = list(data.values())[0]
            columns = list(first_currency.keys())

        self._convert_to_csv(data)

        columns = [key for key in self._currencies["USD"]]

        with open("./files/result_in_csv.csv", "w") as file:
            writer = csv.DictWriter(f=file, fieldnames=columns)

            writer.writeheader()

            writer.writerows(row for row in self._currencies)
