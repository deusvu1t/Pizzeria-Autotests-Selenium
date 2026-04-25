import logging
import sys
from pathlib import Path

LOG_DIR = Path("reports/logs")
LOG_FILE = LOG_DIR / "test_run.log"
LOG_FORMAT = "[%(levelname)s][%(asctime)s][%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
PROJECT_HANDLER_ATTR = "_pizzeria_project_handler"


def setup_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    if any(
        getattr(handler, PROJECT_HANDLER_ATTR, False)
        for handler in root_logger.handlers
    ):
        return

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    setattr(console_handler, PROJECT_HANDLER_ATTR, True)

    file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    setattr(file_handler, PROJECT_HANDLER_ATTR, True)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("selenium").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
