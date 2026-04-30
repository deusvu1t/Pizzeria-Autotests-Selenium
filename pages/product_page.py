from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class ProductPage(BasePage):
    PATH = "/product/"
    NAME = (By.CSS_SELECTOR, ".product_title")
    PRICE = (By.CSS_SELECTOR, ".price .amount")
    BOARD_PACK = (By.ID, "board_pack")
    ADD_TO_CART = (By.CSS_SELECTOR, "button[type='submit'].single_add_to_cart_button")

    def open_product(self, slug: str):
        url = self.BASE_URL + self.PATH + slug
        self.logger.info(f"Открытие URL: {url}")
        self.driver.get(url)

    @property
    def name(self) -> str:
        return self.get_text(self.NAME)

    @property
    def price(self) -> str:
        return self.get_text(self.PRICE)

    def select_board(self, board: str):
        self.logger.info(f"Выбор бортика: {board}")
        select = Select(self.find(self.BOARD_PACK))
        select.select_by_visible_text(board)

    def add_to_cart(self):
        self.click(self.ADD_TO_CART)
