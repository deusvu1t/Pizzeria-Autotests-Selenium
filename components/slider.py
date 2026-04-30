from selenium.webdriver.common.by import By

from components.base_component import BaseComponent
from components.slide import Slide


class Slider(BaseComponent):
    TRACK = (By.CSS_SELECTOR, ".slick-track")
    PREV_BUTTON = (By.CLASS_NAME, "slick-prev")
    NEXT_BUTTON = (By.CLASS_NAME, "slick-next")
    ACTIVE_SLIDE = (By.XPATH, ".//li[contains(@class, 'slick-active')][{index}]")

    def wait_for_animation(self):
        self.logger.debug("Ожидание окончания анимации слайдера")
        track = self.find(self.TRACK)
        self.wait.until(
            lambda d: "transition" not in (track.get_attribute("style") or "")
        )

    def get_slide(self, index: int) -> Slide:
        by, xpath = self.ACTIVE_SLIDE
        element = self.find((by, xpath.format(index=index)))
        return Slide(element, self.page)

    def prev(self):
        self.get_slide(1).hover_self()
        self.click(self.PREV_BUTTON)
        self.wait_for_animation()

    def next(self, last_visible_index: int = 4):
        self.get_slide(last_visible_index).hover_self()
        self.click(self.NEXT_BUTTON)
        self.wait_for_animation()
