import asyncio

import fastapi

app = fastapi.FastAPI()


@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(1)
    return {"message": "Hello, World!"}
