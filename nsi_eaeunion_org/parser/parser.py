import asyncio
from playwright.async_api import async_playwright
from config import settings


class Parser:
    def __init__(self):
        self.url = settings.PARSER_URL


class ParserNSI(Parser):
    def __init__(self):
        super().__init__()


async def parser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # await page.goto('http://playwright.dev')
        await page.goto(settings.PARSER_URL)
        await page.screenshot(path="example-screenshot.png")
        await browser.close()
