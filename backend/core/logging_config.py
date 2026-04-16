import logging
from logging.config import dictConfig


def configure_logging() -> None:
    """
    Configure application-wide logging.
    Idempotent: safe to call multiple times.
    """
    if logging.getLogger().handlers:
        # Already configured
        return

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }

    dictConfig(config)

