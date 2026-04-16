import pytest


import pytest


@pytest.mark.asyncio
async def test_protected_route(client):
    # ✅ Register user (test isolation)
    await client.post(
        "/auth/register",
        json={
            "email": "protected@example.com",
            "password": "password123",
        },
    )

    # ✅ Login
    login = await client.post(
        "/auth/login",
        json={
            "email": "protected@example.com",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    # ✅ Call protected endpoint
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_protected_without_token(client):
    response = await client.get("/users/me")
    assert response.status_code == 403 or response.status_code == 401
