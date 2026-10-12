import asyncio
import time


async def fake_request(name: str) -> str:
    print(f"{name} 请求开始")
    # time.sleep(1) # 这样会阻塞线程，导致无法并发执行
    await asyncio.sleep(1)
    print(f"{name} 请求结束")
    return f"{name}请求结果"


async def main() -> None:

    start = time.perf_counter()

    reuslts = await asyncio.gather(
        fake_request("请求A"),
        fake_request("请求B"),
        fake_request("请求C"),
    )

    end = time.perf_counter()

    duration = end - start

    print(f"耗时：{duration:.2f}秒")
    print(reuslts)


asyncio.run(main())
