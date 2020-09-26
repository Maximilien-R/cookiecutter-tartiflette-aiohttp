from typing import Callable

import pytest

from {{cookiecutter.project_slug}}.server.factory import create_app


@pytest.fixture
def app_client(
    loop: "AbstractEventLoop", aiohttp_client: Callable
) -> "aiohttp.test_utils.TestClient":
    """
    Generates and returns an aiohttp TestClient linked to the application.
    :param loop: an event loop instance
    :param aiohttp_client: callable in charge of creating an aiohttp TestClient
    :type loop: AbstractEventLoop
    :type aiohttp_client: Callable
    :return: an aiohttp TestClient linked to the application
    :rtype: aiohttp.test_utils.TestClient
    """
    return loop.run_until_complete(aiohttp_client(create_app()))
