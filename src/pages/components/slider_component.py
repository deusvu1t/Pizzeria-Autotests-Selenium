import allure
from selenium.webdriver.common.by import By

from src.pages.components.base_component import BaseComponent
from src.pages.components.slide_component import SlideComponent
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SliderComponent(BaseComponent):
    SLIDES = (By.CSS_SELECTOR, ".slick-slide.slick-active")
    TRACK = (By.CLASS_NAME, "slick-track")
    PREV = (By.CLASS_NAME, "slick-prev")
    NEXT = (By.CLASS_NAME, "slick-next")

    def slides(self) -> list[SlideComponent]:
        return [SlideComponent(self.driver, s) for s in self.find_all(self.SLIDES)]

    def slide_titles(self) -> list[str]:
        return [slide.title for slide in self.slides()]

    def _wait_until_animation_finished(self):
        self.wait.until_not(
            lambda _: "slick-animating" in self.find(self.TRACK).get_attribute("class")
        )

    def _move_slider(self, direction_locator, target_slide_index: int):

        before_titles = self.slide_titles()

        self._wait_until_animation_finished()

        self.slides()[target_slide_index].hover()

        self.click(direction_locator)

        self.wait.until(lambda _: self.slide_titles() != before_titles)

        self._wait_until_animation_finished()

    def next(self):
        with allure.step("Переключить слайдер вправо"):
            self._move_slider(self.NEXT, target_slide_index=-1)

    def prev(self):
        with allure.step("Переключить слайдер влево"):
            self._move_slider(self.PREV, target_slide_index=0)
