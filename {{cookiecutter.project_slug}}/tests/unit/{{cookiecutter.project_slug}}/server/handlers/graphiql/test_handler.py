from unittest.mock import Mock, patch, mock_open

import pytest

from {{cookiecutter.project_slug}}.server.handlers.graphiql.handler import (
    _get_graphiql_template,
    handle_graphiql,
)


def test_get_graphiql_template():
    open_mock = mock_open()
    with patch("{{cookiecutter.project_slug}}.server.handlers.graphiql.handler.open", open_mock):
        _get_graphiql_template()
        open_mock.assert_called_once_with(
            "/usr/src/app/{{cookiecutter.project_slug}}/server/handlers/graphiql/templates/graphiql.html"  # pylint: disable=line-too-long
        )
        template_file_mock = open_mock()
        template_file_mock.read.assert_called_once()


@pytest.mark.asyncio
async def test_handle_graphiql():
    request_mock = Mock()
    template_mock = "<html>_get_graphiql_template</html>"

    with patch(
        "{{cookiecutter.project_slug}}.server.handlers.graphiql.handler._get_graphiql_template",
        return_value=template_mock,
    ) as get_graphiql_template_mock:
        response = await handle_graphiql(request_mock)
        get_graphiql_template_mock.assert_called_once()
        assert response.status == 200
        assert response.body.decode("utf-8") == template_mock
        assert dict(response.headers) == {
            "Content-Type": "text/html; charset=utf-8"
        }
