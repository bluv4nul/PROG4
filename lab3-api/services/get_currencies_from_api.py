import httpx
import xml.etree.ElementTree as ET
from models.models import Currency


async def get_currencies_from_api(
    url="https://www.cbr.ru/scripts/XML_daily.asp",
) -> list[Currency]:

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

    data = ET.fromstring(response.text)

    currencies = []

    for valute in data.findall("Valute"):
        code = valute.find("CharCode")
        name = valute.find("Name")
        value = valute.find("Value")

        if code is None or name is None or value is None or value.text is None:
            raise ValueError("Некорректные данные в XML")

        currencies.append(
            Currency(
                code=code.text,
                name=name.text,
                value=float(value.text.replace(",", ".")),
            )
        )

    return currencies
