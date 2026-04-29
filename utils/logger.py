import logging
import os

LOG_FORMAT = "[%(levelname)s][%(asctime)s][%(name)s] %(message)s"
LOG_FILE = os.path.join("logs", "test_run.log")


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    # Защита от повторного добавления хендлеров
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    os.makedirs("logs", exist_ok=True)

    formatter = logging.Formatter(LOG_FORMAT)

    # Консоль — уровень INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Файл — уровень DEBUG
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
