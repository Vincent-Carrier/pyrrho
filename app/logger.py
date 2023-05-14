import logging
import sys
from dataclasses import dataclass
from functools import lru_cache

# LOGGER_FILE = DATA_DIR.joinpath("mealie.log")
DATE_FORMAT = "%d-%b-%y %H:%M:%S"
LOGGER_FORMAT = "%(levelname)s: %(asctime)s \t%(message)s"
LOGGER_HANDLER = None


@dataclass
class LoggerConfig:
    handlers: list
    format: str
    date_format: str
    logger_file: str
    level: str = logging.INFO # type: ignore


@lru_cache
def get_logger_config():
    # if not settings.PRODUCTION:
    from rich.logging import RichHandler

    return LoggerConfig(
        handlers=[RichHandler(rich_tracebacks=True)],
        format=None, # type: ignore
        date_format=None, # type: ignore
        logger_file=None, # type: ignore
    )

    output_file_handler = logging.FileHandler(LOGGER_FILE)
    handler_format = logging.Formatter(LOGGER_FORMAT, datefmt=DATE_FORMAT)
    output_file_handler.setFormatter(handler_format)

    # Stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(handler_format)

    return LoggerConfig(
        handlers=[output_file_handler, stdout_handler],
        format="%(levelname)s: %(asctime)s \t%(message)s",
        date_format="%d-%b-%y %H:%M:%S",
        logger_file=LOGGER_FILE,
    )


logger_config = get_logger_config()

logging.basicConfig(
    level=logger_config.level,
    format=logger_config.format,
    datefmt=logger_config.date_format,
    handlers=logger_config.handlers,
)
