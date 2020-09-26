import pytest

from aiohttp import payload

_HELLO_QUERY = 'query Hello { hello(name: "{{cookiecutter.author_name}}") }'

_EXPECTED_RESPONSE = {"data": {"hello": "Hello {{cookiecutter.author_name}}!"}}


@pytest.mark.parametrize(
    "method,content_type,body,query_params",
    [
        # Content-Type: application/graphql
        (
            "get",
            "application/graphql",
            None,
            {"query": _HELLO_QUERY},
        ),
        (
            "post",
            "application/graphql",
            None,
            {"query": _HELLO_QUERY},
        ),
        (
            "post",
            "application/graphql",
            _HELLO_QUERY,
            None,
        ),
        # Content-Type: application/json
        (
            "get",
            "application/json",
            payload.JsonPayload({}),
            {"query": _HELLO_QUERY},
        ),
        (
            "post",
            "application/json",
            payload.JsonPayload({}),
            {"query": _HELLO_QUERY},
        ),
        (
            "post",
            "application/json",
            payload.JsonPayload({"query": _HELLO_QUERY}),
            None,
        ),
        # Content-Type: application/x-www-form-urlencoded
        (
            "get",
            "application/x-www-form-urlencoded",
            None,
            {"query": _HELLO_QUERY},
        ),
        (
            "post",
            "application/x-www-form-urlencoded",
            None,
            {"query": _HELLO_QUERY},
        ),
        (
            "post",
            "application/x-www-form-urlencoded",
            {"query": _HELLO_QUERY},
            None,
        ),
    ],
)
async def test_handle_graphql(
    app_client, method, content_type, body, query_params
):
    response = await (
        getattr(app_client, method)(
            "/graphql",
            data=body,
            params=query_params,
            headers={"content-type": content_type},
        )
    )

    assert response.status == 200
    assert await response.json() == _EXPECTED_RESPONSE
