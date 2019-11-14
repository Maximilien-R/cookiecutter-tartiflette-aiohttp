async def test_handle_ready(app_client):
    response = await app_client.get("/health/ready")
    assert response.status == 200
    assert await response.text() == "OK"
