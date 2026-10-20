# ========== 1. 搭服务骨架 ==========

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

app = FastAPI(title="day07-FastAPI")


@app.get("/health")
async def check_health():
    return {"status": "ok"}


# @app.get("/news/{id}")
# async def get_news(id: int = Path(..., ge=1, le=100, description="新闻id")):
#     return {"id": id, "title": f"新闻分类id 是{id}"}


class ChatMessage(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ChatService:
    def reply(self, message: str) -> str:
        return f"收到：{message}"


def get_chat_service() -> ChatService:
    return ChatService()


@app.post("/chat")
async def chat(
    body: ChatMessage, service: Annotated[ChatService, Depends(get_chat_service)]
) -> dict[str, str]:
    if not body.message.strip():
        return HTTPException(status_code=400, detail="message 不能为空")

    return {"reply": service.reply(body.message)}


# 统一错误处理
# 校验失败进入的错误拦截
@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc) -> JSONResponse:

    details = [
        {"field": ".".join(str(part) for part in error["loc"]), "message": error["msg"]}
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "请求参数校验失败",
                "details": details,
            }
        },
    )


# 处理 HTTP error
@app.exception_handler(HTTPException)
def http_error_handler(request: Request, exc) -> JSONResponse:

    return JSONResponse()
