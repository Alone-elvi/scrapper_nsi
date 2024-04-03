import asyncio
import requests

from datetime import datetime as dt

from playwright.async_api import async_playwright
from config import settings


def find_values_by_keys(data, target_keys):
    """
    Находит все значения для заданных ключей на всех уровнях вложенности словаря.

    :param data: Словарь или список для поиска.
    :param target_keys: Список ключей, для которых нужно найти значения.
    :return: Список найденных значений.
    """
    found_values = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key in target_keys:
                found_values.append(value)
            # Рекурсивно ищем в значениях, если они являются словарями или списками
            found_values.extend(find_values_by_keys(value, target_keys))
    elif isinstance(data, list):
        # Если текущий объект является списком, итерируем по его элементам
        for item in data:
            found_values.extend(find_values_by_keys(item, target_keys))

    return found_values


class Parser:
    def __init__(self, url: str):
        self.browser = None
        self.page = None
        self.url = url


class ParserAPI(Parser):
    def __init__(self, url: str = settings.PARSER_API_URL):
        super().__init__(url)
        self.response = None
        self.parser_data = []

    def get_browser(self) -> None:
        pass

    def send_api_request(self, offset: int = 0) -> None:
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        settings.PARSER_API_PARAMS["offset"] = offset
        self.response = requests.post(
            self.url, json=settings.PARSER_API_PARAMS, verify=False, headers=headers
        )

    async def parse_data(self) -> None:

        row_data = []
        for rows in self.parser_data:
            row_data.extend(
                find_values_by_keys(row, settings.PARSER_API_DATA_TITLES)
                for row in rows
            )

        return row_data

    async def write_to_excel(self, row_data):
        import pandas as pd

        df = pd.DataFrame(row_data, columns=settings.PARSER_API_DATA_TITLES_RUS)

        # Запись DataFrame в файл Excel
        file_path = f"people_data-{dt.now().strftime('%Y-%m-%d-%H-%M-%S')}.xlsx"  # Укажите ваш путь и имя файла
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        print(f"Данные успешно записаны в файл {file_path}")


class ParserNSI(Parser):
    def __init__(self, url: str = settings.PARSER_URL):
        super().__init__(url)
        # self.browser = self.get_browser()
        # self.page = self.set_page()
        self.table = None

    async def get_browser(self) -> None:
        ap = await async_playwright().start()
        self.browser = await ap.chromium.launch()

    async def close_browser(self) -> None:
        await self.browser.close()

    async def set_page(self) -> None:
        self.page = await self.browser.new_page()

    async def get_page(self) -> None:
        return await self.browser.new_page()

    async def close_page(self) -> None:
        await self.page.close()

    async def go_to_page(self) -> None:
        return await self.page.goto(
            self.url, wait_until=settings.PARSER_PARAMS["wait_until"]
        )

    async def get_table(self) -> None:
        self.table = await self.page.query_selector(settings.PARSER_PARAMS["table"])

    async def get_title(self) -> None:
        return await self.page.title()

    async def set_url(self, url: str) -> None:
        self.url = await url

    async def get_table_nodes(self, selector) -> None:
        return list(
            await self.table.eval_on_selector_all(
                selector, "nodes => nodes.map(node => node.innerText)"
            )
        )

    async def get_elements(self, attribute, selector) -> None:
        elements = (
            self.page.get_by_role(selector).and_(self.page.locator(attribute)).last
        )
        return await elements.all_inner_texts()


async def parser():
    parser = ParserNSI(settings.PARSER_URL)
    await parser.get_browser()
    await parser.set_page()
    await parser.go_to_page()

    # await parser.get_table()

    # for index, elem in enumerate(await parser.get_table_nodes("td")):
    #     if index % 9 == 0:
    #         print("\n")
    #     print(elem, end=" | ")

    parser_api = ParserAPI()
    print(parser_api.url)
    parser_api.parser_data = []
    pages = await parser.get_elements(
        settings.PARSER_API_DATA_MAX_PAGES_TAG,
        settings.PARSER_API_DATA_MAX_PAGES_SELECTOR,
    )
    for index in range(int(pages[0]) + 1):
        parser_api.send_api_request((index) * 16)
        parser_api.parser_data.append(parser_api.response.json())

    await parser_api.write_to_excel(await parser_api.parse_data())

    print("finish")

    # print(await parser.get_title())
    # table = parser.get_table()
    # print(await table)
    # for row in await table.query_selector_all("tr"):
    #     print(await row.inner_text())
    #     for cell in await row.query_selector_all("td"):
    #         print(await cell.inner_text())
    # await parser.page.screenshot(path="example-screenshot.png")

    # pars_table = page.locator('tbody.p-datatable-tbody')
    # for row in await pars_table.all_inner_texts():
    #     print(row)
    #     for cell in row:
    #         print(cell)

    await parser.close_browser()
