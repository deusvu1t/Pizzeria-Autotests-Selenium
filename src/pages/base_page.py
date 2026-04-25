from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, timeout=settings.timeout)

    # ─── НАВИГАЦИЯ ───────────────────────────────────────────────────────────

    def open(self, path: str = "") -> None:
        """Открыть страницу по относительному пути."""
        url = f"{settings.base_url}{path}"
        logger.info("Opening page | url=%s", url)
        self._driver.get(url)
        logger.debug(
            "Page opened | title=%s | url=%s",
            self._driver.title,
            self._driver.current_url,
        )

    def get_current_url(self) -> str:
        url = self._driver.current_url
        logger.debug("Current url=%s", url)
        return url

    def get_title(self) -> str:
        title = self._driver.title
        logger.debug("Page title=%s", title)
        return title

    # ─── Поиск элементов на странице ─────────────────────────────────────────

    def find(self, locator: tuple) -> WebElement:
        logger.debug("Find for element | locator=%s", locator)
        element = self._driver.find_element(*locator)
        logger.debug("Element found | locator=%s", locator)
        return element

    # ─── ОЖИДАНИЯ ────────────────────────────────────────────────────────────

    def wait_for_element(self, locator: tuple) -> WebElement:
        """Ждать появления и видимости элемента."""
        logger.debug("Waiting for element | locator=%s", locator)
        try:
            element = self._wait.until(EC.visibility_of_element_located(locator))
            logger.debug("Element found | locator=%s", locator)
            return element
        except TimeoutException:
            logger.error(
                "Element not found after %ss | locator=%s", settings.timeout, locator
            )
            raise

    def wait_for_element_invisible(self, locator: tuple) -> bool:
        """Ждать исчезновения элемента."""
        logger.debug("Waiting for element to disappear | locator=%s", locator)
        try:
            result = self._wait.until(EC.invisibility_of_element_located(locator))
            logger.debug("Element disappeared | locator=%s", locator)
            return result
        except TimeoutException:
            logger.error(
                "Element still visible after %ss | locator=%s",
                settings.timeout,
                locator,
            )
            raise

    def wait_for_url(self, expected_url: str) -> None:
        """Ждать смены URL."""
        logger.debug("Waiting for url | expected=%s", expected_url)
        try:
            self._wait.until(EC.url_contains(expected_url))
            logger.debug("URL matched | current=%s", self._driver.current_url)
        except TimeoutException:
            logger.error(
                "URL did not change after %ss | expected=%s | current=%s",
                settings.timeout,
                expected_url,
                self._driver.current_url,
            )
            raise

    def wait_and_click(self, locator: tuple) -> None:
        """Ждать кликабельности и кликнуть."""
        logger.debug("Waiting for element to be clickable | locator=%s", locator)
        try:
            element = self._wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logger.debug("Clicked after wait | locator=%s", locator)
        except TimeoutException:
            logger.error(
                "Element not clickable after %ss | locator=%s",
                settings.timeout,
                locator,
            )
            raise

    # ─── ДЕЙСТВИЯ С ЭЛЕМЕНТАМИ ───────────────────────────────────────────────

    def click(self, locator: tuple) -> None:
        """Найти элемент и кликнуть."""
        logger.debug("Click | locator=%s", locator)
        self.wait_for_element(locator).click()

    def type_text(self, locator: tuple, text: str) -> None:
        """Очистить поле и ввести текст."""
        logger.debug("Type text | locator=%s | text=%s", locator, text)
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """Получить текст элемента."""
        text = self.wait_for_element(locator).text
        logger.debug("Got text | locator=%s | text=%s", locator, text)
        return text

    def is_visible(self, locator: tuple) -> bool:
        """Проверить видимость элемента без выброса исключения."""
        try:
            return self._driver.find_element(*locator).is_displayed()
        except NoSuchElementException:
            logger.debug("Element not visible | locator=%s", locator)
            return False

    def scroll_to(self, locator: tuple) -> WebElement:
        """Прокрутить страницу к элементу."""
        logger.debug("Scrolling to element | locator=%s", locator)
        element = self.wait_for_element(locator)
        ActionChains(self._driver).scroll_to_element(element).perform()
        return element
