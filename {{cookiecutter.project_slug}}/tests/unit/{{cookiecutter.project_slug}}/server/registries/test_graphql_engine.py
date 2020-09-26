from unittest.mock import AsyncMock, Mock, patch

import pytest

from {{cookiecutter.project_slug}}.server.registries import graphql_engine, register_graphql_engine


@pytest.mark.asyncio
async def test_register_graphql_engine():
    app_mock = {}

    graphql_engine_mock = Mock()
    graphql_engine_mock.cook = AsyncMock()

    with patch.object(
        graphql_engine, "_GRAPHQL_ENGINE", new=graphql_engine_mock
    ):
        assert "graphql_engine" not in app_mock
        await register_graphql_engine(app_mock)
        assert app_mock["graphql_engine"] is graphql_engine_mock
        graphql_engine_mock.cook.assert_awaited_once()
