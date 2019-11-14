async def test_handle_live(app_client):
    response = await app_client.get("/health/live")
    assert response.status == 200
    assert await response.text() == "OK"
