import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from src.pages.base_page import BasePage
from src.utils.helpers import normalize_text, parse_price
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ProductPage(BasePage):
    TITLE = (By.CLASS_NAME, "product_title")
    PRICE = (By.CSS_SELECTOR, ".summary bdi")
    BOARD_PACK = (By.NAME, "board_pack")
    ADD_BTN = (By.CSS_SELECTOR, ".summary .button ")

    def open(self, part):
        return super().open(part)

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

    @property
    def active_board_pack(self) -> str:
        select_element = self.find(self.BOARD_PACK)
        # Возвращает текст выбранного option
        return Select(select_element).first_selected_option.text

    @property
    def active_board_pack_value(self) -> str:
        with allure.step("Получить value активного борта"):
            val = Select(
                self.find(self.BOARD_PACK)
            ).first_selected_option.get_attribute("value")
            return val if val else ""

    @allure.step("Выбрать борт пиццы: {name}")
    def board_pack(self, name: str):
        logger.info("Selecting board pack: %s", name)
        select = Select(self.find(self.BOARD_PACK))
        for option in select.options:
            if name in option.text:
                select.select_by_visible_text(option.text)
                return
        raise ValueError(f"Option with text '{name}' not found")

    def add_to_cart(self):
        self.click(self.ADD_BTN)
