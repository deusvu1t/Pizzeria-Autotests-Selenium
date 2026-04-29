import allure

from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    URL = None

    def __init__(self, driver):
        if not self.URL:
            raise ValueError("Page requires a non-empty url")

        self.driver = driver
        self.url = self.URL
        self.timeout = 10

    def open(self):
        with allure.step(f"Открытие страницы {self.url}"):
            logger.info(f"Opening URL: {self.url}")
            self.driver.get(self.url)
