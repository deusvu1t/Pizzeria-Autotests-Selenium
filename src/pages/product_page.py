import allure
from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage
from src.utils.helpers import normalize_text, parse_price
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ProductPage(BasePage):
    TITLE = (By.CLASS_NAME, "product_title")
    PRICE = (By.CSS_SELECTOR, ".summary bdi")

    @property
    def title(self) -> str:
        with allure.step("Получить название продукта"):
            title = self.wait.until(lambda _: self.find(self.TITLE).text.strip())
            logger.info("Product name | %s", title)
            return normalize_text(title)

    @property
    def price(self) -> float:
        with allure.step("Получить цену продукта"):
            price = self.wait.until(lambda _: self.find(self.PRICE).text.strip())
            logger.info("Product price | %s", price)
            return parse_price(price)
