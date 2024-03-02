from fastapi import FastAPI
import redis.asyncio as redis
import httpx

app = FastAPI()


async def get_redis():
    r = await redis.from_url("redis://localhost:6379")
    return r


@app.post("/pub")
async def pub_to_redis(channel: str, text: str):
    r = await get_redis()
    print("redis connected")
    for _ in range(5):
        await r.publish(channel, text)
    await r.publish(channel, "STOP")
    return {"response": "all task is done"}
