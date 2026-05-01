import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class ProductPage(BasePage):
    PATH = "/product/"
    NAME = (By.CSS_SELECTOR, ".product_title")
    PRICE = (By.CSS_SELECTOR, ".price .amount")
    BOARD_PACK = (By.ID, "board_pack")
    ADDED_TO_CART_MESSAGE = (By.CSS_SELECTOR, ".woocommerce-message")
    VIEW_CART = (By.CSS_SELECTOR, ".woocommerce-message a")
    ADD_TO_CART = (By.CSS_SELECTOR, "button[type='submit'].single_add_to_cart_button")

    @property
    def name(self) -> str:
        return self.get_text(self.NAME)

    @property
    def price(self) -> str:
        return self.get_text(self.PRICE)

    @property
    def board_options(self) -> list[str]:
        select = Select(self.find(self.BOARD_PACK))
        return [option.text for option in select.options]

    @property
    def selected_board(self) -> str:
        select = Select(self.find(self.BOARD_PACK))
        return select.first_selected_option.text

    @allure.step("Выбрать борт: {board}")
    def select_board(self, board: str):
        Select(self.find(self.BOARD_PACK)).select_by_visible_text(board)

    @allure.step("Добавить товар в корзину со страницы продукта")
    def add_to_cart(self):
        self.click(self.ADD_TO_CART)
        self.find(self.ADDED_TO_CART_MESSAGE)

    @allure.step("Перейти в корзину из сообщения об успехе")
    def go_to_cart_from_message(self):
        self.click(self.VIEW_CART)
