import pytest

from aiohttp.test_utils import make_mocked_request

from {{cookiecutter.project_slug}}.server.handlers.health import handle_ready


@pytest.mark.asyncio
async def test_handle_ready():
    response = await handle_ready(make_mocked_request("GET", "/health/ready"))
    assert response.status == 200
    assert response.text == "OK"
