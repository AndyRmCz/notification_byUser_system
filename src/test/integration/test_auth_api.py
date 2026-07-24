import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_auth_register_api(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "fresh@domain.com", "password": "Password123!"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == "fresh@domain.com"

@pytest.mark.asyncio
async def test_auth_login_api(client: AsyncClient):

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "developer@test.com", "password": "SecretPassword123"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()