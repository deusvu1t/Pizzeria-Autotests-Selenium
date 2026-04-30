from selenium.webdriver.common.by import By

from components.base_component import BaseComponent


class NavPanel(BaseComponent):
    NAV_LINK = (By.CSS_SELECTOR, "nav a[href*='{path}']")
    CART_ICON = (By.CSS_SELECTOR, "a.cart-contents")
    CART_TOTAL = (By.CSS_SELECTOR, ".amount")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='my-account']")

    def go_to(self, path: str):
        self.logger.info(f"Переход в навигации: {path}")
        by, css = self.NAV_LINK
        self.click((by, css.format(path=path)))

    @property
    def cart_total(self) -> str:
        return self.get_text(self.CART_TOTAL)

    def go_to_cart(self):
        self.click(self.CART_ICON)

    def go_to_login(self):
        self.click(self.LOGIN_LINK)
