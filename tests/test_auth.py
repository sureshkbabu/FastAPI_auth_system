import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    # Register
    response = await client.post(
        "/auth/register",
        json={
            "email": "testuser@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201

    # Login
    response = await client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data