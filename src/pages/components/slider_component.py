from selenium.webdriver.common.by import By

from src.pages.components.base_component import BaseComponent
from src.pages.components.slide_component import SlideComponent


class SliderComponent(BaseComponent):
    SLIDES = (By.CSS_SELECTOR, "li[aria-hidden='false']")

    def slides(self) -> list[SlideComponent]:
        return [
            SlideComponent(self.driver, slide) for slide in self.find_all(self.SLIDES)
        ]
