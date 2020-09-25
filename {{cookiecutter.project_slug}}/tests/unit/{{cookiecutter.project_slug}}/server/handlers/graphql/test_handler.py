import json

from unittest.mock import Mock, patch

import pytest

from asynctest import CoroutineMock

from {{cookiecutter.project_slug}}.server.handlers.graphql.handler import _prepare_response, handle_graphql


@pytest.mark.parametrize(
    "result,status,headers,expected_response,expected_headers",
    [
        (
            {},
            200,
            None,
            json.dumps({"data": None}).encode("utf-8"),
            {"Content-Type": "application/json; charset=utf-8"},
        ),
        (
            {"unknown": "value"},
            200,
            None,
            json.dumps({"data": None}).encode("utf-8"),
            {"Content-Type": "application/json; charset=utf-8"},
        ),
        (
            {"data": None},
            200,
            None,
            json.dumps({"data": None}).encode("utf-8"),
            {"Content-Type": "application/json; charset=utf-8"},
        ),
        (
            {"data": {"field": "value"}},
            200,
            None,
            json.dumps({"data": {"field": "value"}}).encode("utf-8"),
            {"Content-Type": "application/json; charset=utf-8"},
        ),
        (
            {
                "data": {"field": "value"},
                "errors": [{"message": "Error"}],
                "extensions": {"extra": "value"},
            },
            400,
            {"header1": "value1"},
            json.dumps(
                {
                    "data": {"field": "value"},
                    "errors": [{"message": "Error"}],
                    "extensions": {"extra": "value"},
                }
            ).encode("utf-8"),
            {
                "Content-Type": "application/json; charset=utf-8",
                "header1": "value1",
            },
        ),
    ],
)
def test_prepare_response(
    result, status, headers, expected_response, expected_headers
):
    response = _prepare_response(result, status, headers)
    assert response.status == status
    assert dict(response.headers) == expected_headers
    assert response.body == expected_response


@pytest.mark.asyncio
async def test_handle_graphql():
    query = '{ hello(name: "{{cookiecutter.author_name}}") }'
    expected_response = {"data": None}

    request_mock = Mock()
    request_mock.app = {"graphql_engine": Mock()}
    request_mock.app["graphql_engine"].execute = CoroutineMock(
        return_value=expected_response
    )

    with patch(
        "{{cookiecutter.project_slug}}.server.handlers.graphql.handler.extract_graphql_params",
        new_callable=CoroutineMock,
        return_value=(query, None, None),
    ) as extract_graphql_params_mock:
        with patch(
            "{{cookiecutter.project_slug}}.server.handlers.graphql.handler._prepare_response",
            return_value=expected_response,
        ) as prepare_response_mock:
            response = await handle_graphql(request_mock)
            assert response == expected_response
            extract_graphql_params_mock.assert_awaited_once_with(request_mock)
            request_mock.app[
                "graphql_engine"
            ].execute.assert_awaited_once_with(
                query,
                operation_name=None,
                variables=None,
                context={"request": request_mock},
            )
            prepare_response_mock.assert_called_once_with(expected_response)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "extracted_graphql_params,expected_status_code,expected_error",
    [
        (
            (None, None, None),
            400,
            {
                "message": "400, message='Must provide query string.'",
                "path": None,
                "locations": [],
            },
        ),
        (
            RuntimeError("An error occurred."),
            500,
            {"message": "An error occurred.", "path": None, "locations": []},
        ),
    ],
)
async def test_handle_graphql_exception(
    extracted_graphql_params, expected_status_code, expected_error
):
    request_mock = Mock()
    with patch(
        "{{cookiecutter.project_slug}}.server.handlers.graphql.handler.extract_graphql_params",
        new_callable=CoroutineMock,
        side_effect=[extracted_graphql_params],
    ) as extract_graphql_params_mock:
        with patch(
            "{{cookiecutter.project_slug}}.server.handlers.graphql.handler._prepare_response",
            wraps=_prepare_response,
        ) as prepare_response_mock:
            response = await handle_graphql(request_mock)
            extract_graphql_params_mock.assert_awaited_once_with(request_mock)
            prepare_response_mock.assert_called_once_with(
                {"errors": [expected_error]},
                status=expected_status_code,
            )
            assert response.status == expected_status_code
            assert response.body == json.dumps(
                {"data": None, "errors": [expected_error]}
            ).encode("utf-8")
