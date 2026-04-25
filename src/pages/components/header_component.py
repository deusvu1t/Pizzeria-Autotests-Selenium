from selenium.webdriver.common.by import By

from src.pages.components.base_component import BaseComponent


class HeaderComponent(BaseComponent):
    CART_CONTENTS = (By.CLASS_NAME, "cart-contents")

    @property
    def title(self) -> str:
        return self.wait.until(lambda _: self.find(self.CART_CONTENTS).text.strip())
