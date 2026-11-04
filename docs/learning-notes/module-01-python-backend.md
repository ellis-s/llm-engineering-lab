# 模块 1：Python 后端与服务工程

## 模块目标

能独立搭建一个 FastAPI 服务，处理请求校验、依赖、统一错误、异步调用和流式响应，并用测试验证关键行为。

## 核心笔记

### 类型标注与运行时校验

- **一句话结论：** Python 类型标注主要帮助阅读、IDE 和静态检查；它本身不会自动拦住运行时的错误输入。
- **为什么 / 何时用：** 外部 JSON、环境变量等不可信输入，要在边界使用 Pydantic 等运行时校验。
- **易错点：** 函数写了 name: str，不代表运行时传入 123 会自动报错。
- **代码或项目：** [day1_concepts.py](../../01-python-backend/00-python-engineering/day1_concepts.py)

### Pydantic 与 dataclass

- **一句话结论：** Pydantic 模型擅长校验和解析边界数据；dataclass 轻量表达应用内部的数据结构。
- **易错点：** 两者都能承载字段，但不能因此认为它们默认承担相同的输入校验职责。
- **关联：** HTTP JSON → Pydantic 请求模型 → 业务服务内部对象。

### FastAPI 请求体与依赖注入

- **一句话结论：** body: ChatMessage 表示请求数据；Annotated[ChatService, Depends(get_chat_service)] 表示由 FastAPI 提供的依赖。
- **易错点：** 不要把 Depends(get_chat_service) 放到请求体参数上；普通 JSON 接口直接返回字典即可，StreamingResponse 留给流式端点。
- **代码或项目：** [day03_validation/main.py](../../01-python-backend/01-fastapi/day03_validation/main.py)

### 400、422 与 500

- **一句话结论：** 请求结构或字段约束失败通常是 422；请求通过结构校验但违反业务规则可返回 400；未预期的程序错误应返回 500。
- **易错点：** min_length=1 拒绝空字符串，但 "   " 长度不为零；需要 strip() 才能识别纯空白。
- **安全提醒：** 记录服务端异常细节用于排查，返回给客户端的 500 信息保持稳定，不泄露堆栈或内部数据。

### async、协程与 await

- **一句话结论：** 调用 async def 会得到协程；需要 await 才会等待协程运行并取得结果。
- **易错点：** 裸写 asyncio.sleep(1) 只创建协程，不会按预期等待；在异步路径中使用 time.sleep(1) 会阻塞事件循环。
- **关联：** I/O 等待时让出执行权 → 事件循环可运行其他任务 → 并发提高 I/O 利用率。
- **代码或项目：** [main.py](../../01-python-backend/02-async/day04_concurrency/main.py)

### HTTPX 客户端、超时与重试

- **一句话结论：** 并发请求复用一个 httpx.AsyncClient；为请求设超时；只对可恢复的超时/网络错误做有限重试。
- **易错点：** 不要无限重试，也不要把所有 HTTP 状态错误都当作网络故障重试；退避等待也要用 await asyncio.sleep(...)。
- **代码或项目：** [day04_httpx.py](../../01-python-backend/02-async/day04_concurrency/day04_httpx.py)

### SSE 事件格式与浏览器消费

- **一句话结论：** SSE 通过 text/event-stream 持续发送文本事件；字段行后以空行结束一个事件。
- **易错点：** event: token 是自定义事件名，浏览器要用 addEventListener("token", ...) 接收；收到完成事件后应关闭 EventSource。
- **心跳：** 冒号开头的是注释，客户端忽略内容；只有连接长时间没有业务数据时才真正有保活意义。
- **关联：** 异步生成器逐段 yield → StreamingResponse → 浏览器逐事件消费。

### pytest、API 测试和依赖替换

- **一句话结论：** TestClient 能直接调用 FastAPI 应用，不需要另启 Uvicorn；测试名以 test_ 开头，使用断言验证行为。
- **易错点：** 改写 app.dependency_overrides 后要清理替换，防止污染其他测试。
- **代码或项目：** [test_main.py](../../01-python-backend/01-fastapi/day03_validation/test_main.py)

### 覆盖率

- **一句话结论：** 覆盖率显示测试执行到了哪些代码行或分支，不等于测试断言正确，也不等于系统没有缺陷。
- **复习动作：** 查看未覆盖行，判断它是重要行为分支、错误分支还是无需测试的代码，再决定是否补用例。

## 我犯过的错

| 现象 | 原因 | 以后如何快速识别 |
|---|---|---|
| coroutine was never awaited，任务耗时意外接近 0 | 调用了异步函数但没有 await | 检查每个异步调用是否被等待或被任务调度 |
| time.sleep 让并发任务串行等待 | 阻塞了事件循环所在的线程 | I/O 等待用异步库和 await |
| 注释掉 SSE 心跳没有明显变化 | 模拟 token 每隔很短时间就有数据，连接本来就活跃 | 心跳价值看空闲时间，不看事件条数 |

## 主动回忆题

先不看上面的笔记回答；模块测验会从这些问题和实际代码中抽查。

1. 为什么类型标注不能替代 Pydantic 请求校验？
2. /chat 中哪些错误该是 422，哪些可用 400？
3. 为什么 await asyncio.sleep() 不会像 time.sleep() 一样阻塞所有协程？
4. 什么情况下重试网络请求合理？为什么不能对所有异常无限重试？
5. SSE 的事件由什么分隔？浏览器如何区分 token 和 done 事件？
6. 使用 FastAPI TestClient 时，为什么通常不需要启动 Uvicorn？
7. 100% 行覆盖率能证明什么、不能证明什么？

## 复习记录

| 日期 | 结果 / 需要补强的点 |
|---|---|
| 2026-11-02 | 建立本模块复习卡；学员决定暂缓 Day 7 周测剩余内容与模块测验，直接进入模块 2 |
