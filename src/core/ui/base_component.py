from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BaseComponent:
    def __init__(self, driver: WebDriver, root: WebElement):
        self._driver = driver
        self._wait = WebDriverWait(driver, timeout=Settings.timeout)
        self._root = root
