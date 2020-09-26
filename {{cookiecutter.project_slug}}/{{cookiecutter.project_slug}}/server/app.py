from aiohttp import web

from {{cookiecutter.project_slug}}.server.factory import create_app

__all__ = ("run_app",)


def run_app() -> int:
    """Entry point of the application.

    :return: application exit code
    :rtype: int
    """
    web.run_app(
        create_app(),
        host="0.0.0.0",  # nosec
        port=8090,
        handle_signals=True,
    )
    return 0
