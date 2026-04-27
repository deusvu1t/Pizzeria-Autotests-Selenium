import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.logger import get_logger

logger = get_logger(__name__)


class BaseComponent:
    def __init__(self, driver, root, timeout=10):
        self.driver = driver
        self.root = root
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        logger.debug("Find element | locator=%s", locator)
        return self.wait.until(lambda _: self.root.find_element(*locator))

    def find_all(self, locator):
        logger.debug("Find elements | locator=%s", locator)
        return self.wait.until(lambda _: self.root.find_elements(*locator))

    def click(self, locator: tuple[str, str]):
        logger.info("Click | locator=%s", locator)
        with allure.step(f"Кликнуть по элементу: {locator}"):
            # Re-fetch element inside the lambda to avoid StaleElementReferenceException
            # if the root or element goes stale while waiting for it to be clickable
            def _find_and_check_clickable(driver):
                try:
                    el = self.root.find_element(*locator)
                    if el.is_displayed() and el.is_enabled():
                        return el
                except Exception:
                    pass
                return False

            element = self.wait.until(_find_and_check_clickable)
            element.click()

    def hover(self):
        logger.info("Hover | %s", self.__class__.__name__)
        with allure.step(f"Навести курсор: {self.__class__.__name__}"):
            self.wait.until(lambda _: self.root.is_displayed())
            ActionChains(self.driver).move_to_element(self.root).perform()

    def is_displayed(self) -> bool:
        name = self.__class__.__name__
        logger.debug("Check visibility for: %s", name)
        try:
            return bool(self.wait.until(lambda _: self.root.is_displayed()))
        except TimeoutException:
            logger.warning("Component %s not visible after timeout", name)
            return False

    def is_visible(self, locator: tuple[str, str]) -> bool:
        logger.debug("Check element visibility | locator=%s", locator)
        try:
            return bool(self.wait.until(lambda _: self.find(locator).is_displayed()))
        except TimeoutException:
            logger.warning("Element %s not visible after timeout", locator)
            return False
