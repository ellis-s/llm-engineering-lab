from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="day2 - FastAPI")


@app.get("/health")
def check_health() -> dict[str, str]:
    return {"status": "ok"}


"""
正常调用, 返回200
curl -i http://127.0.0.1:8000/echo?message=hello

不带参数，返回 422
curl -i http://127.0.0.1:8000/echo

"""


@app.get("/echo")
def echo(message: str) -> dict[str, str]:
    return {"message": message}


class ChatMessage(BaseModel):
    message: str


# curl -i -X POST http://127.0.0.1:8000/chat -H "Content-Type:application/json" -d '{"message": "你好"}'
@app.post("/chat")
def chat(request: ChatMessage) -> dict[str, str]:
    return {"reply": f"收到：{request.message}"}
