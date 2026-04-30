from selenium.webdriver.common.by import By

from components.cart_item import CartItem
from pages.base_page import BasePage
from utils.helpers import normalize_text


class CartPage(BasePage):
    PATH = "/cart/"
    CART_ITEM = (By.CLASS_NAME, "cart_item")

    def get_cart_items(self) -> list[CartItem]:
        return [CartItem(el, self) for el in self.find_all(self.CART_ITEM)]

    def find_item(self, name: str, variation: str | None = None) -> CartItem | None:
        items = self.get_cart_items()
        for item in items:
            name_match = normalize_text(item.name) == normalize_text(name)
            variation_match = item.variation == variation
            if name_match and variation_match:
                return item
        return None
