import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_create_and_fetch_notifications_api(client: AsyncClient):
    # 1. Create a notification
    payload = {
        "title": "System Alert",
        "content": "Deployment successfully executed.",
        "channel": "push",
        "recipient": "token-device-string-12345"
    }
    create_res = await client.post("/api/v1/notifications/", json=payload)
    assert create_res.status_code == status.HTTP_201_CREATED
    created_id = create_res.json()["id"]

    # 2. List notifications
    list_res = await client.get("/api/v1/notifications/")
    assert list_res.status_code == status.HTTP_200_OK
    assert len(list_res.json()) >= 1

    # 3. Delete notification
    del_res = await client.delete(f"/api/v1/notifications/{created_id}")
    assert del_res.status_code == status.HTTP_204_NO_CONTENT