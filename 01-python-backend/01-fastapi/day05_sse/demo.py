"""
学习 time.sleep 和 asyncio.sleep 的区别。

只是初步的了解，还没深入学习。

1. 在异步函数中是不能使用同步的 time.sleep 函数的. 否则会会阻塞线程，导致无法并发执行。

"""

import asyncio
import time


def sync_sleep(name: str):
    print(f"任务：{name}")
    time.sleep(1)


async def async_sleep(name: str):
    print(f"任务：{name}")
    await asyncio.sleep(1)


async def main():
    start = time.perf_counter()

    # 1. 把同步的 time.sleep 函数改为异步的 asyncio.sleep
    # 放到三个线程中，它们之间就是并发执行了，互不阻塞

    # await asyncio.gather(
    #     asyncio.to_thread(sync_sleep, "任务1"),
    #     asyncio.to_thread(sync_sleep, "任务2"),
    #     asyncio.to_thread(sync_sleep, "任务3"),
    # )

    # 2. 三个任务之间会阻塞。
    # try:
    #     await asyncio.gather(
    #         sync_sleep("任务1"),
    #         sync_sleep("任务2"),
    #         sync_sleep("任务3"),
    #     )
    # except Exception as exception:
    #     print(f"异常：{exception}")

    # 3. 正确写法，三个任务之间互不阻塞。相当于是 js 中的 Promise.all()
    await asyncio.gather(
        async_sleep("任务1"),
        async_sleep("任务2"),
        async_sleep("任务3"),
    )

    usetime = time.perf_counter() - start
    print(f"耗时：{usetime:.2f}s")


asyncio.run(main())
