import allure

from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    def __init__(self, driver, url="https://pizzeria.skillbox.cc/"):
        self.driver = driver
        self.url = url
        self.timeout = 10

    @allure.step("Открытие страницы {url}")
    def open(self, url=None):
        target_url = url if url else self.url
        logger.info(f"Opening URL: {target_url}")
        self.driver.get(target_url)
