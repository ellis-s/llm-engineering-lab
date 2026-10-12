import asyncio
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI(title="day5 - SSE")


@app.get("/chat/stream")
async def stream_chat() -> StreamingResponse:
    async def generate() -> AsyncIterator[str]:
        tokens = ["你好", "，", "这是", "一段", "模拟流式回复。"]

        try:
            for index, token in enumerate(tokens, start=1):
                # SSE 事件以空行结束；data 是发给客户端的数据
                yield f"event: token\nid: {index}\ndata: {token}\n\n"
                await asyncio.sleep(0.5)

                # 冒号开头的是注释，客户端忽略它，可用于保持连接
                if index % 2 == 0:
                    yield ": keep-alive\n\n"

            yield "event: done\ndata: [DONE]\n\n"
        finally:
            print("流生成器已结束，清理连接相关资源")

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/", response_class=HTMLResponse)
async def get_index() -> str:
    return """
    <!doctype html>
    <html lang="zh-CN">
      <meta charset="utf-8">
      <title>SSE 演示</title>
      <body>
        <button id="start">开始接收</button>
        <pre id="output"></pre>
        <script>
          document.querySelector("#start").onclick = () => {
            const output = document.querySelector("#output");
            output.textContent = "";

            const source = new EventSource("/chat/stream");

            source.addEventListener("token", (event) => {
              output.textContent += event.data;
            });

            source.addEventListener("done", () => {
              source.close();
              output.textContent += "\\n[流结束]";
            });

            source.onerror = () => {
              output.textContent += "\\n[连接发生错误]";
              source.close();
            };
          };
        </script>
      </body>
    </html>
  """
