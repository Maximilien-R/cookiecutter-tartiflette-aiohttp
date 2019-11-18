async def test_handle_graphql(app_client):
    response = await app_client.get("/graphiql")
    assert response.status == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert "React.createElement(GraphiQL" in await response.text()
