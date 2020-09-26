from asyncio import AbstractEventLoop
from typing import Callable

import pytest

from aiohttp.test_utils import TestClient

from {{cookiecutter.project_slug}}.server.factory import create_app


@pytest.fixture
def app_client(
    loop: AbstractEventLoop, aiohttp_client: Callable
) -> TestClient:
    """Return an aiohttp TestClient linked to the application.

    :param loop: an event loop instance
    :param aiohttp_client: callable creating the aiohttp TestClient
    :type loop: AbstractEventLoop
    :type aiohttp_client: Callable
    :return: an aiohttp TestClient linked to the application
    :rtype: TestClient
    """
    return loop.run_until_complete(aiohttp_client(create_app()))
