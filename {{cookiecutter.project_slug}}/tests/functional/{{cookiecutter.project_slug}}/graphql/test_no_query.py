import pytest


@pytest.mark.parametrize("method", ["get", "post"])
async def test_handle_graphql_no_query_application_graphql(app_client, method):
    response = await (
        getattr(app_client, method)(
            "/graphql",
            headers={"content-type": "application/graphql"},
        )
    )

    assert response.status == 400
    assert await response.json() == {
        "data": None,
        "errors": [
            {
                "message": "400, message='Must provide query string.'",
                "path": None,
                "locations": [],
            },
        ],
    }


@pytest.mark.parametrize("method", ["get", "post"])
async def test_handle_graphql_no_query_application_json(app_client, method):
    response = await (
        getattr(app_client, method)(
            "/graphql",
            json={},
            headers={"content-type": "application/json"},
        )
    )

    assert response.status == 400
    assert await response.json() == {
        "data": None,
        "errors": [
            {
                "message": "400, message='Must provide query string.'",
                "path": None,
                "locations": [],
            },
        ],
    }


@pytest.mark.parametrize("method", ["get", "post"])
async def test_handle_graphql_no_query_application_form_urlencoded(
    app_client, method
):
    response = await (
        getattr(app_client, method)(
            "/graphql",
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
    )

    assert response.status == 400
    assert await response.json() == {
        "data": None,
        "errors": [
            {
                "message": "400, message='Must provide query string.'",
                "path": None,
                "locations": [],
            },
        ],
    }
