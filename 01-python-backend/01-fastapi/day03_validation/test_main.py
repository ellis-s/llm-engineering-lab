"""
# 如何运行
uv run pytest -v test_main.py


day06 的文件

"""

from fastapi.testclient import TestClient
from main import ChatService, app, get_chat_service

client = TestClient(app)


def test_health_response_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_reply():
    response = client.post("/chat", json={"message": "hello"})

    assert response.status_code == 200
    assert response.json() == {"reply": ChatService().reply("hello")}


def test_whitespace_message_returns_400():
    response = client.post("/chat", json={"message": " "})

    assert response.status_code == 400
    json = response.json()

    assert json["error"]["code"] == "HTTP_400"
    assert json["error"]["message"] == "message can not be empty"


def test_empty_message_returns_422():
    response = client.post("/chat", json={"message": ""})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_non_string_message_returns_422():
    response = client.post("/chat", json={"message": 123})

    assert response.status_code == 422


def test_missing_message_returns_422():
    response = client.post("/chat", json={})

    assert response.status_code == 422

    json = response.json()
    assert json["error"]["code"] == "VALIDATION_ERROR"
    assert json["error"]["message"] == "请求参数校验失败"
    assert isinstance(json["error"]["details"], list)
    assert json["error"]["details"][0]["field"] == "body.message"


def test_message_over_2000_returns_422():
    message = "a" * 2001
    response = client.post("/chat", json={"message": message})

    assert response.status_code == 422

    json = response.json()
    assert json["error"]["code"] == "VALIDATION_ERROR"
    assert json["error"]["message"] == "请求参数校验失败"
    assert isinstance(json["error"]["details"], list)


def test_message_at_max_length_is_accepted():
    message = "a" * 2000
    response = client.post("/chat", json={"message": message})

    assert response.status_code == 200
    assert response.json()["reply"] == f"收到：{message}"


def test_chat_uses_replaced_service():
    class FakeChatService:
        def reply(self, message: str) -> str:
            return f"测试回复：{message}"

    app.dependency_overrides[get_chat_service] = FakeChatService

    try:
        response = client.post("/chat", json={"message": "你好"})
    finally:
        app.dependency_overrides.pop(get_chat_service, None)

    assert response.status_code == 200
    assert response.json() == {"reply": "测试回复：你好"}


def test_chat_service_reply():
    service = ChatService()

    assert service.reply("你好") == "收到：你好"
