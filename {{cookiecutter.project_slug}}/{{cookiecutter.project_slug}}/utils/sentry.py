import logging.config

import sentry_sdk

from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from {{cookiecutter.project_slug}}.config import config

__all__ = ("configure_sentry",)


def configure_sentry() -> None:
    """
    Configure sentry client from config files.
    """
    sentry_sdk.init(
        dsn=config["sentry"]["dsn"],
        integrations=[
            LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR,
            ),
            AioHttpIntegration(),
        ]
    )
