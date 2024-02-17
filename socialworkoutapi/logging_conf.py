from logging.config import dictConfig

from socialworkoutapi.config import DevConfig, config


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {  # asgi_correlation_id.CorrelationIdFilter(uuid_length=8, default_value="-")
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if isinstance(config, DevConfig) else 32,
                    "default_value": "-"

                }
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s"
                },
                "file": {
                    # pip install python-json-logger (for JSON output)
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s %(msecs)04d %(levelname)-8s %(correlation_id)s %(name)s %(lineno)d %(message)s"
                }
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",  # pip install rich (for datetime en colors output)
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id"]
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filename": "socialworkoutapi.log",
                    "maxBytes": 1024 * 1024,  # 1MB
                    "backupCount": 2,  # how many files
                    "encoding": "utf8",
                    "filters": ["correlation_id"]
                }
            },
            "loggers": {
                "uvicorn": {"handlers": ["default", "rotating_file"], "level": "INFO"},
                "databases": {"handlers": ["default"], "level": "WARNING"},
                "aiosqlite": {"handlers": ["default"], "level": "WARNING"},
                "socialworkoutapi": {
                    "handlers": ["default", "rotating_file"],
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    # propagate = False : dont send to the root logger (e.g. root.socialworkoutapi.routers.post)
                    "propagate": False
                }
            }
        }
    )
