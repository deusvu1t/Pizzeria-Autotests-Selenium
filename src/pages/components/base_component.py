from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


class BaseComponent:
    def __init__(self, driver, root, timeout=10):
        self.driver = driver
        self.root = root
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        return self.wait.until(lambda _: self.root.find_element(*locator))

    def find_all(self, locator):
        return self.wait.until(lambda _: self.root.find_elements(*locator))

    def click(self, locator: tuple[str, str]):
        self.find(locator).click()

    def hover(self):
        self.wait.until(lambda _: self.root.is_displayed())
        ActionChains(self.driver).move_to_element(self.root).perform()

    def is_displayed(self, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda _: self.root.is_displayed()
            )
            return True
        except TimeoutException:
            return False

    def is_visible(self, locator: tuple[str, str], timeout: int = 10) -> bool:
        try:
            self.wait.until(lambda _: self.find(locator).is_displayed())
            return True
        except TimeoutException:
            return False
