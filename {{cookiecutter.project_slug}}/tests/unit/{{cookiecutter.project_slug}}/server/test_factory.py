from unittest.mock import Mock, patch

import pytest

from {{cookiecutter.project_slug}}.server.factory import create_app
from {{cookiecutter.project_slug}}.server.registries import register_graphql_engine


@pytest.mark.asyncio
async def test_create_app():
    app_mock = Mock()
    app_mock.on_startup = []

    with patch("{{cookiecutter.project_slug}}.server.factory.web.Application", return_value=app_mock):
        with patch("{{cookiecutter.project_slug}}.server.factory.register_routes") as register_routes_mock:
            assert await create_app() == app_mock
            register_routes_mock.assert_called_once_with(app_mock)
            assert register_graphql_engine in app_mock.on_startup
