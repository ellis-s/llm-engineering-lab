import asyncio
import logging
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# ---------- 1. 应用与路由 ----------
app = FastAPI(title="day07-FastAPI")
router = APIRouter()


# ---------- 2. 请求 / 响应模型 ----------
class ChatMessage(BaseModel):
    message: str = Field(min_length=1, max_length=2000)

    # @field_validator("message")
    # @classmethod
    # def strip_message(cls, value: str) -> str:
    #     value = value.strip()
    #     if not value:
    #         raise ValueError("message 不能为空")
    #     return value


class ChatResponse(BaseModel):
    reply: str


# ---------- 3. 业务服务与依赖 ----------
class ChatService:
    def reply(self, message: str) -> str:
        return f"收到：{message}"


def get_chat_service() -> ChatService:
    return ChatService()


# ---------- 4. 路由 ----------
@router.get("/health")
async def check_health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
async def chat(
    body: ChatMessage,
    service: Annotated[ChatService, Depends(get_chat_service)],
) -> ChatResponse:
    if not body.message.strip():
        raise HTTPException(status_code=400, detail="message 不能为空")

    return ChatResponse(reply=service.reply(body.message))


async def generate_tokens() -> AsyncIterator[str]:
    tokens = ["你好", "，", "这是", "一段", "流式回复。"]

    try:
        for token in tokens:
            yield f"event: token\ndata: {token}\n\n"
            await asyncio.sleep(0.4)

        yield "event: done\ndata: [DONE]\n\n"
    finally:
        logger.info("SSE 生成器已结束")


@router.get("/chat/stream")
async def chat_stream() -> StreamingResponse:
    return StreamingResponse(
        generate_tokens(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/mock/http/error")
async def mock_http_error():
    """
    模拟业务异常
    """
    raise HTTPException(
        status_code=400,
        detail="模拟http错误，你不是 VIP 用户，所以我让你看到我这个模拟错误！",
    )


# ---------- 5. 统一错误响应 ----------
def make_error(code: str, message: str, details: list | None = None) -> dict:
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details or [],
        }
    }


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    框架（自动检查）
    """
    details = [
        {
            "field": ".".join(str(part) for part in error["loc"]),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content=make_error("VALIDATION_ERROR", "请求参数校验失败", details),
    )


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(
    _request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """
    程序员（主动抛出）
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=make_error(f"HTTP_{exc.status_code}", str(exc.detail)),
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, _exc: Exception) -> JSONResponse:
    """
    系统/Bug （意外崩溃）
    """
    logger.exception("未处理异常: %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content=make_error("INTERNAL_SERVER_ERROR", "服务器内部错误"),
    )


# ---------- 6. 注册路由 ----------
app.include_router(router)
