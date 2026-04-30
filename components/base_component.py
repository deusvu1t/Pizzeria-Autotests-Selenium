# components/base_component.py
from selenium.webdriver.remote.webelement import WebElement


class BaseComponent:
    def __init__(self, element: WebElement, page):
        self.element = element
        self.page = page
        self.wait = page.wait
        self.logger = page.logger

    def find(self, locator):
        return self.page.find_in(locator, self.element)

    def find_all(self, locator):
        return self.page.find_all_in(locator, self.element)

    def find_optional(self, locator):
        elements = self.element.find_elements(*locator)
        return elements[0] if elements else None

    def click(self, locator):
        self.page.click_in(locator, self.element)

    def hover(self, element):
        self.page.hover(element)

    def hover_self(self):
        self.page.hover(self.element)

    def get_text(self, locator) -> str:
        text = self.find(locator).text
        self.logger.debug(f"Получен текст из элемента: {locator} → '{text}'")
        return text
