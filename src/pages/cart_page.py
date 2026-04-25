from src.core.ui.base_page import BasePage


class CartPage(BasePage):
    def open(self, path: str = "cart/") -> None:
        return super().open(path)
