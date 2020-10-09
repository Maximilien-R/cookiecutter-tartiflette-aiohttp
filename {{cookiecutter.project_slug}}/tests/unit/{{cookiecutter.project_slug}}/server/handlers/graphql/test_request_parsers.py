from unittest.mock import AsyncMock, Mock, patch

import pytest

from aiohttp.http_exceptions import HttpBadRequest

from {{cookiecutter.project_slug}}.server.handlers.graphql.request_parsers import (
    _extract_multipart_params,
    _form_data_request_parser,
    _form_urlencoded_request_parser,
    _graphql_request_parser,
    _inject_file_to_operations,
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
async def test_form_urlencoded_request_parser():
    payload = {"query": '{ hello(name: "{{cookiecutter.author_name}}") }'}

    request = Mock()
    request.post = AsyncMock(return_value=payload)
    assert await _form_urlencoded_request_parser(request) == payload


@pytest.mark.parametrize(
    "operations,file_instance,path",
    [
        (
            {"variables": {"file": None}},
            None,
            "variables.file",
        ),
        (
            {"variables": {"file": None}},
            True,
            "variables.file",
        ),
        (
            {"variables": {"file": None}},
            Mock(),
            "variables.file",
        ),
        (
            {"variables": {"files": [None]}},
            None,
            "variables.files.0",
        ),
        (
            {"variables": {"files": [None]}},
            True,
            "variables.files.0",
        ),
        (
            {"variables": {"files": [None]}},
            Mock(),
            "variables.files.0",
        ),
    ],
)
def test_inject_file_to_operations(operations, file_instance, path):
    response = _inject_file_to_operations(
        operations, file_instance, path.split("."), path
    )

    for key in path.split("."):
        try:
            key = int(key)
        except ValueError:
            pass
        response = response[key]

    assert response is file_instance


@pytest.mark.parametrize(
    "operations,path,expected",
    [
        (
            {"variables": {"file": True}},
            "variables.file",
            (
                "Path < variables.file > in < map > multipart field doesn't "
                "lead to a null value."
            ),
        ),
        (
            {"variables": {"files": None}},
            "variables.files.0",
            (
                "Index < 0 > from path < variables.files.0 > doesn't lead to "
                "a list."
            ),
        ),
        (
            {"variables": {"files": {}}},
            "variables.files.0",
            (
                "Index < 0 > from path < variables.files.0 > doesn't lead to "
                "a list."
            ),
        ),
        (
            {"variables": None},
            "variables.file",
            (
                "Key < file > from path < variables.file > doesn't lead to an "
                "object."
            ),
        ),
        (
            {"variables": []},
            "variables.file",
            (
                "Key < file > from path < variables.file > doesn't lead to an "
                "object."
            ),
        ),
    ],
)
def test_inject_file_to_operations_error(operations, path, expected):
    with pytest.raises(HttpBadRequest, match=f'400, message="{expected}"'):
        _inject_file_to_operations(operations, Mock(), path.split("."), path)


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {"operations": "{}", "map": "{}"},
            ({}, {}),
        ),
        (
            {
                "operations": '{"query": "query"}',
                "map": '{"0": ["variables.0"]}',
            },
            (
                {"query": "query"},
                {"0": ["variables.0"]},
            ),
        ),
    ],
)
def test_extract_multipart_params(data, expected):
    assert _extract_multipart_params(data) == expected


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {},
            "Missing multipart field < operations >.",
        ),
        (
            {"operations": None},
            "Missing multipart field < map >.",
        ),
        (
            {"operations": None, "map": None},
            "Invalid JSON in the < operations > multipart field.",
        ),
        (
            {"operations": "[/]", "map": None},
            "Invalid JSON in the < operations > multipart field.",
        ),
        (
            {"operations": "[]", "map": None},
            "Invalid type for the < operations > multipart field.",
        ),
        (
            {"operations": "true", "map": None},
            "Invalid type for the < operations > multipart field.",
        ),
        (
            {"operations": "{}", "map": None},
            "Invalid JSON in the < map > multipart field.",
        ),
        (
            {"operations": "{}", "map": "[/]"},
            "Invalid JSON in the < map > multipart field.",
        ),
        (
            {"operations": "{}", "map": "[]"},
            "Invalid type for the < map > multipart field.",
        ),
        (
            {"operations": "{}", "map": "true"},
            "Invalid type for the < map > multipart field.",
        ),
    ],
)
def test_extract_multipart_params_error(data, expected):
    with pytest.raises(HttpBadRequest, match=f"400, message='{expected}'"):
        _extract_multipart_params(data)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {
                "operations": '{"query": "{}"}',
                "map": "{}",
            },
            {"query": "{}"},
        ),
        (
            {
                "operations": '{"query": "{}", "variables": {"file": null}}',
                "map": '{"0": ["variables.file"]}',
                "0": "file0",
            },
            {"query": "{}", "variables": {"file": "file0"}},
        ),
        (
            {
                "operations": (
                    '{"query": "{}", "variables": {"files": [null, null]}}'
                ),
                "map": (
                    '{"0": ["variables.files.0"], "1": ["variables.files.1"]}'
                ),
                "0": "file0",
                "1": "file1",
            },
            {"query": "{}", "variables": {"files": ["file0", "file1"]}},
        ),
        (
            {
                "operations": (
                    '{"query": "{}", "variables": {"files": [null, null]}}'
                ),
                "map": '{"0": ["variables.files.0", "variables.files.1"]}',
                "0": "file0",
            },
            {"query": "{}", "variables": {"files": ["file0", "file0"]}},
        ),
        (
            {
                "operations": (
                    '{"query": "{}",'
                    '"variables": {"file": null, "files": [null, null, null]}}'
                ),
                "map": (
                    '{"0": ["variables.file", "variables.files.1"], '
                    '"1": ["variables.files.0"], '
                    '"2": ["variables.files.2"]}'
                ),
                "0": "file0",
                "1": "file1",
                "2": "file2",
            },
            {
                "query": "{}",
                "variables": {
                    "file": "file0",
                    "files": ["file1", "file0", "file2"],
                },
            },
        ),
    ],
)
async def test_form_data_request_parser(data, expected):
    request = Mock()
    request.post = AsyncMock(return_value=data)
    assert await _form_data_request_parser(request) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {
                "operations": '{"query": "{}", "variables": {"file": null}}',
                "map": '{"0": {}}',
                "0": "file0",
            },
            (
                "Invalid type for the < map > multipart field entry key < 0 > "
                "array."
            ),
        ),
        (
            {
                "operations": '{"query": "{}", "variables": {"file": null}}',
                "map": '{"0": [null]}',
                "0": "file0",
            },
            (
                "Invalid type for the < map > multipart field entry key "
                "< 0 > array index < 0 > value."
            ),
        ),
        (
            {
                "operations": '{"query": "{}", "variables": {"file": null}}',
                "map": '{"0": ["variables.file", true]}',
                "0": "file0",
            },
            (
                "Invalid type for the < map > multipart field entry key "
                "< 0 > array index < 1 > value."
            ),
        ),
    ],
)
async def test_form_data_request_parser_error(data, expected):
    request = Mock()
    request.post = AsyncMock(return_value=data)

    with pytest.raises(HttpBadRequest, match=f"400, message='{expected}'"):
        await _form_data_request_parser(request)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "content_type,method_called,return_value,expected",
    [
        (
            "application/graphql",
            "text",
            "text",
            {"query": "text"},
        ),
        (
            "application/json",
            "json",
            "json",
            "json",
        ),
        (
            "application/x-www-form-urlencoded",
            "post",
            "post",
            "post",
        ),
        (
            "multipart/form-data",
            "post",
            {"operations": '{"query": "post"}', "map": "{}"},
            {"query": "post"},
        ),
    ],
)
async def test_parse_request(
    content_type, method_called, return_value, expected
):
    request = Mock(content_type=content_type)
    setattr(request, method_called, AsyncMock(return_value=return_value))
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
