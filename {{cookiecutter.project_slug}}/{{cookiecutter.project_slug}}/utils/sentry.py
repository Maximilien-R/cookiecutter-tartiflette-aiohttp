import logging
import logging.config

from typing import Any, Dict

import sentry_sdk

from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from {{cookiecutter.project_slug}}.config import config

__all__ = ("configure_sentry", "sentry_error_coercer")

logger = logging.getLogger(__name__)


def configure_sentry() -> None:
    """
    Configure sentry client from config files.
    """
    sentry_sdk.init(
        dsn=config["sentry"]["dsn"],
        integrations=[
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
            AioHttpIntegration(),
        ],
    )


async def sentry_error_coercer(
    exception: Exception, error: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Sends original error of the exception to Sentry.
    :param exception: exception raised
    :param error: coerced error
    :type exception: Exception
    :type error: Dict[str, Any]
    :return: the coerced error
    :rtype: Dict[str, Any]
    """
    original_error = getattr(exception, "original_error", None)
    if isinstance(original_error, Exception):
        if not sentry_sdk.capture_exception(original_error):
            logger.exception("Unhandled error.", exc_info=original_error)
    return error
