import pytest

from aiohttp.test_utils import make_mocked_request

from {{cookiecutter.project_slug}}.server.handlers.health import handle_live


@pytest.mark.asyncio
async def test_handle_live():
    response = await handle_live(make_mocked_request("GET", "/health/live"))
    assert response.status == 200
    assert response.text == "OK"
