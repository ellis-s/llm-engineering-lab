from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_reply():
    response = client.post("/chat", json={"message": "你好"})

    assert response.status_code == 200
    assert response.json() == {"reply": "收到：你好"}
