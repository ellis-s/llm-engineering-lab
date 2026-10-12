import asyncio
import time

import httpx

# async def main() -> None:

#     async with httpx.AsyncClient(timeout=2.0) as client:
#         response = await client.get("http://127.0.0.1:8000/health")
#         response.raise_for_status()

#         print("状态码:", response.status_code)
#         print("响应内容:", response.json())


# asyncio.run(main())


# API_URL = "http://127.0.0.1:8001/slow"
API_URL = "http://127.0.0.1:8000/health"


async def fetch_health(client: httpx.AsyncClient, request_id: int):

    max_attampts = 3

    for attempt in range(1, max_attampts + 1):
        try:
            print(f"请求{request_id}=====第{attempt}次请求")
            response = await client.get(API_URL)
            response.raise_for_status()

            # 如果请求成功，则直接 return ，就不会再次循环尝试了
            return {
                "status_code": response.status_code,
                "body": response.json(),
                "request_id": request_id,
            }
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            if attempt == max_attampts:
                print(f"请求{attempt}次，仍然失败")
                raise

            delay = 0.2 * attempt
            print(
                f"请求 {request_id} 第 {attempt} 次失败：{type(exc).__name__}，"
                f"{delay:.1f}s 后重试"
            )
            await asyncio.sleep(delay)


async def main() -> None:

    start = time.perf_counter()
    # httpx 建议共用一个client，以利用连接池
    async with httpx.AsyncClient(timeout=httpx.Timeout(None, connect=0.5)) as client:
        result = await asyncio.gather(*(fetch_health(client, i) for i in range(10)))
        # result = await asyncio.gather(fetch_health(client, 1))

        usetime = time.perf_counter() - start

        print(f"耗时：{usetime:.2f}s")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
