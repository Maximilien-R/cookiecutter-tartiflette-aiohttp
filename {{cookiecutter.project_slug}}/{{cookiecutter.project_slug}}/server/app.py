import logging

from aiohttp import web

from {{cookiecutter.project_slug}}.server.factory import create_app

__all__ = ("run_app",)

logger = logging.getLogger(__name__)


def run_app() -> int:
    """Entry point of the application.

    :return: application exit code
    :rtype: int
    """
    logger.debug("App is live.")
    web.run_app(
        create_app(),
        host="0.0.0.0",  # nosec
        port=8090,
        handle_signals=True,
    )
    logger.debug("App is stopped.")
    return 0
