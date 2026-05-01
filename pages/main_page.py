from selenium.webdriver.common.by import By

from components.slider import Slider
from pages.base_page import BasePage


class MainPage(BasePage):
    PATH = "/"
    _PIZZA_SLIDER = (By.ID, "product1")

    @property
    def pizza_slider(self) -> Slider:
        return Slider(self.find(self._PIZZA_SLIDER), self)
