import logging.config

from {{cookiecutter.project_slug}}.config import config

__all__ = ("configure_logging",)


def configure_logging() -> None:
    """
    Configure logging using a dictionary from config files.
    """
    logging.config.dictConfig(config["logging"])
