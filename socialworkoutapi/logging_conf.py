from logging.config import dictConfig

from socialworkoutapi.config import DevConfig, config


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(name)s:%(lineno)d - %(message)s"
                }
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",  # pip install rich (for datetime en colors output)
                    "level": "DEBUG",
                    "formatter": "console"
                }
            },
            "loggers": {  # propagate = False : dont send to the root logger (e.g. root.socialworkoutapi.routers.post)
                "socialworkoutapi": {
                    "handlers": ["default"],
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False
                }
            }
        }
    )
