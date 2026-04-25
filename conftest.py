from src.utils.logger import get_logger, setup_logging

logger = get_logger(__name__)


def pytest_configure(config):
    setup_logging()


def pytest_addoption(parser):
    parser.addoption("--browser", default=None)
    parser.addoption("--run-mode", default=None)
    parser.addoption("--headless", action="store_true", default=None)


pytest_plugins: list[str] = [
    "src.fixtures.driver",
    "src.fixtures.pages",
]
