from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    print(response.json().get("Hello"))
    assert response.json().get("Hello") == "World"
    assert response.status_code == 200
    # data = response.json()

