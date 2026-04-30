from selenium.webdriver.common.by import By

from components.base_component import BaseComponent


class NavPanel(BaseComponent):
    MENU_LINK = (By.CSS_SELECTOR, "a[href*='/product-category/menu/']")
    DESSERTS_LINK = (By.CSS_SELECTOR, "a[href*='/product-category/menu/deserts/']")
    CART_ICON = (By.CSS_SELECTOR, "a.cart-contents")
    CART_TOTAL = (By.CSS_SELECTOR, ".amount")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='my-account']")

    @property
    def cart_total(self) -> str:
        return self.get_text(self.CART_TOTAL)

    def go_to_cart(self):
        self.click(self.CART_ICON)

    def go_to_login(self):
        self.click(self.LOGIN_LINK)

    def go_to_deserts(self):
        self.logger.info("Переход в раздел десертов")
        self.hover(self.find(self.MENU_LINK))
        self.click(self.DESSERTS_LINK)
