import pytest
from fastapi.testclient import TestClient
from menu_app.main import app


pytest_plugins = ('pytest_asyncio',)
client = TestClient(app=app)


@pytest.mark.asyncio
async def test_root():
    response = client.get("/api/v1/healthchecker/")
    assert response.status_code == 200
    assert response.json() == {"message": "The API is LIVE!!"}
