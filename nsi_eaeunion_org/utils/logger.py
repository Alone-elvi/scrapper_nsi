import functools
import logging
from logging.handlers import RotatingFileHandler

from utils import check_path
from config import settings


def setup_logging():
    """
    Sets up the logging configuration using the settings in the settings module.
    """    
    
    check_path.check_path(settings.LOGGING_DIR)

    logging.basicConfig(
        level=settings.LOGGING_LEVEL,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                settings.LOGGING_FILE_ERROR,
                maxBytes=1048576,
                backupCount=5,
                encoding="utf-8",
            ),
            logging.StreamHandler(),  # Для вывода в консоль
        ],
    )


def handle_exceptions(func):
    """
    A decorator function to handle exceptions for the input function.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Ошибка в {func.__name__}: {e}")
            raise e

    return wrapper
