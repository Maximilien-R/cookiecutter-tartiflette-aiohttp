from unittest.mock import AsyncMock, Mock, patch

import pytest

from aiohttp.http_exceptions import HttpBadRequest

from {{cookiecutter.project_slug}}.server.handlers.graphql.request_parsers import (
    _form_request_parser,
    _graphql_request_parser,
    _json_request_parser,
    _parse_graphql_params,
    _parse_request,
    extract_graphql_params,
)


@pytest.mark.asyncio
async def test_graphql_request_parser():
    query = '{ hello(name: "{{cookiecutter.author_name}}") }'

    request = Mock()
    request.text = AsyncMock(return_value=query)
    result = await _graphql_request_parser(request)
    assert result == {"query": query}


@pytest.mark.asyncio
async def test_json_request_parser():
    payload = {"query": '{ hello(name: "{{cookiecutter.author_name}}") }'}

    request = Mock()
    request.json = AsyncMock(return_value=payload)
    result = await _json_request_parser(request)
    assert result == payload


@pytest.mark.asyncio
async def test_json_request_parser_invalid_json():
    request = Mock()
    request.json = AsyncMock(side_effect=[Exception()])
    with pytest.raises(
        HttpBadRequest, match="400, message='POST body sent invalid JSON.'"
    ):
        await _json_request_parser(request)


@pytest.mark.asyncio
async def test_form_request_parser():
    payload = {"query": '{ hello(name: "{{cookiecutter.author_name}}") }'}

    request = Mock()
    request.post = AsyncMock(return_value=payload)
    result = await _form_request_parser(request)
    assert result == payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "content_type,method_called,expected",
    [
        (
            "application/graphql",
            "text",
            {"query": "text"},
        ),
        (
            "application/json",
            "json",
            "json",
        ),
        (
            "application/x-www-form-urlencoded",
            "post",
            "post",
        ),
        (
            "multipart/form-data",
            "post",
            "post",
        ),
    ],
)
async def test_parse_request(content_type, method_called, expected):
    request = Mock(content_type=content_type)
    request.text = AsyncMock(return_value="text")
    request.json = AsyncMock(return_value="json")
    request.post = AsyncMock(return_value="post")
    response = await _parse_request(request)
    assert response == expected
    getattr(request, method_called).assert_awaited_once()


@pytest.mark.asyncio
async def test_parse_request_unknown_content_type():
    request = Mock(content_type="unknown")
    response = await _parse_request(request)
    assert response == {}


@pytest.mark.parametrize(
    "body_data,url_data,expected",
    [
        # Empty
        ({}, {}, (None, None, None)),
        # Query
        ({"query": "body_query"}, {}, ("body_query", None, None)),
        ({"query": None}, {}, (None, None, None)),
        ({"query": False}, {}, (None, None, None)),
        ({}, {"query": "url_query"}, ("url_query", None, None)),
        ({}, {"query": None}, (None, None, None)),
        ({}, {"query": False}, (None, None, None)),
        (
            {"query": "body_query"},
            {"query": "url_query"},
            ("url_query", None, None),
        ),
        # Variables
        (
            {"variables": '{"var1": "body_val1"}'},
            {},
            (None, {"var1": "body_val1"}, None),
        ),
        (
            {"variables": {"var1": "body_val1"}},
            {},
            (None, {"var1": "body_val1"}, None),
        ),
        ({"variables": None}, {}, (None, None, None)),
        ({"variables": False}, {}, (None, None, None)),
        (
            {},
            {"variables": '{"var1": "url_val1"}'},
            (None, {"var1": "url_val1"}, None),
        ),
        (
            {},
            {"variables": {"var1": "url_val1"}},
            (None, {"var1": "url_val1"}, None),
        ),
        ({}, {"variables": None}, (None, None, None)),
        ({}, {"variables": False}, (None, None, None)),
        (
            {"variables": '{"var1": "body_val1"}'},
            {"variables": '{"var1": "url_val1"}'},
            (None, {"var1": "url_val1"}, None),
        ),
        (
            {"variables": {"var1": "body_val1"}},
            {"variables": {"var1": "url_val1"}},
            (None, {"var1": "url_val1"}, None),
        ),
        # Operation Name
        (
            {"operationName": "body_operation_name"},
            {},
            (None, None, "body_operation_name"),
        ),
        ({"operationName": None}, {}, (None, None, None)),
        ({"operationName": False}, {}, (None, None, None)),
        (
            {},
            {"operationName": "url_operation_name"},
            (None, None, "url_operation_name"),
        ),
        ({}, {"operationName": None}, (None, None, None)),
        ({}, {"operationName": False}, (None, None, None)),
        (
            {"operationName": "body_operation_name"},
            {"operationName": "url_operation_name"},
            (None, None, "url_operation_name"),
        ),
    ],
)
def test_parse_graphql_params(body_data, url_data, expected):
    assert expected == _parse_graphql_params(body_data, url_data)


@pytest.mark.parametrize(
    "body_data,url_data",
    [
        (
            {"variables": "[/]"},
            {},
        ),
        (
            {},
            {"variables": "[/]"},
        ),
    ],
)
def test_parse_graphql_params_invalid_variables_json(body_data, url_data):
    with pytest.raises(
        HttpBadRequest, match="400, message='Variables are invalid JSON.'"
    ):
        _parse_graphql_params(body_data, url_data)


@pytest.mark.asyncio
async def test_extract_graphql_params():
    parsed_request = {}

    request = Mock()
    request.query = {}

    with patch(
        "{{cookiecutter.project_slug}}.server.handlers.graphql.request_parsers._parse_graphql_params"
    ) as parse_graphql_params_mock:
        with patch(
            "{{cookiecutter.project_slug}}.server.handlers.graphql.request_parsers._parse_request",
            new_callable=AsyncMock,
            return_value=parsed_request,
        ) as parse_request_mock:
            await extract_graphql_params(request)
            parse_request_mock.assert_awaited_once_with(request)
            parse_graphql_params_mock.assert_called_once_with(
                parsed_request, request.query
            )
