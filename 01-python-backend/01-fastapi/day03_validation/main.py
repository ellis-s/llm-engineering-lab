import logging
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="day3 - validation")
logger = logging.getLogger(__name__)


# TODO: 校验失败的时候会触发这个异常处理器，返回错误信息。
# 自定义错误处理器，返回的错误信息格式保持统一。
@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:

    details = [
        {
            "field": ".".join(str(part) for part in error["loc"]),
            "message": error["msg"],
        }
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


# TODO
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": str(exc.detail),
                "details": [],
            }
        },
    )


# TODO 后端服务内部错误，比如语法问题、运行时bug
@app.exception_handler(Exception)
async def unexception_error_handler(request: Request, exc: Exception) -> JSONResponse:

    logger.exception(
        "未处理异常： method=%s path=%s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "服务器内部错误",
                "details": [],
            }
        },
    )


# 中间件执行顺序是洋葱模型。 call_next 之前是自下而上， call_next 之后是自上而下
@app.middleware("http")
async def log_request1(request: Request, call_next):
    print(f"log_request1:::{request.method} {request.url.path}")
    result = await call_next(request)
    print("log_request1  end!")
    return result


@app.middleware("http")
async def log_request2(request: Request, call_next):
    print(f"log_request2==={request.method} {request.url.path}")
    result = await call_next(request)
    print("log_request2  end!")
    return result


class ChatMessage(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


# 把业务逻辑抽离到一个业务服务中
class ChatService:
    def reply(self, message: str) -> str:
        return f"收到：{message}"


def get_chat_service() -> ChatService:
    return ChatService()


"""
Annotated: 是用来给类型附加额外的元数据的。 然后 通过 from typing import get_args 可以获取到这个元数据。有些框架就会利用这个元数据当做一个参数使用。
"""


@app.post("/chat")
def chat(
    request: ChatMessage, service: Annotated[ChatService, Depends(get_chat_service)]
) -> dict[str, str]:

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="message can not be empty")

    return {"reply": service.reply(request.message)}
