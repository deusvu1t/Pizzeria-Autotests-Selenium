from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from components.nav_panel import NavPanel
from utils.logger import get_logger


class BasePage:
    BASE_URL = "https://pizzeria.skillbox.cc"
    PATH = ""
    NAV_PANEL = (By.CSS_SELECTOR, "header")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = get_logger(self.__class__.__name__)

    def open(self, path_suffix: str = ""):
        url = self.BASE_URL + self.PATH + path_suffix
        self.logger.info(f"Открытие URL: {url}")
        self.driver.get(url)

    @property
    def header(self):
        return NavPanel(self.find(self.NAV_PANEL), self)

    def find(self, locator):
        self.logger.debug(f"Поиск элемента: {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        self.logger.debug(f"Поиск всех элементов: {locator}")
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def find_in(self, locator, element: WebElement):
        self.logger.debug(f"Поиск видимого элемента {locator} внутри {element}")

        def condition(_):
            try:
                found = element.find_element(*locator)
                return found if found.is_displayed() else False
            except (NoSuchElementException, StaleElementReferenceException):
                return False

        return self.wait.until(condition)

    def find_all_in(self, locator, element: WebElement):
        self.logger.debug(f"Поиск видимых элементов {locator} внутри {element}")

        def condition(_):
            try:
                elements = element.find_elements(*locator)
                visible = [el for el in elements if el.is_displayed()]
                return visible if visible else False
            except StaleElementReferenceException:
                return False

        return self.wait.until(condition)

    def hover(self, element: WebElement):
        self.logger.debug(f"Наведение на элемент: {element}")
        ActionChains(self.driver).move_to_element(element).perform()

    def click(self, locator):
        self.logger.info(f"Клик по элементу: {locator}")
        self.find(locator).click()

    def click_in(self, locator, element: WebElement):
        self.logger.info(f"Клик по элементу {locator} внутри {element}")
        self.find_in(locator, element).click()

    def get_text(self, locator) -> str:
        text = self.find(locator).text
        self.logger.debug(f"Получен текст '{text}' из элемента: {locator}")
        return text

    def input_text(self, locator, text: str):
        self.logger.debug(f"Ввод текста '{text}' в элемент: {locator}")
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def is_visible(self, locator, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
