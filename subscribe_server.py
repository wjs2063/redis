from fastapi import FastAPI, Depends, WebSocket
import async_timeout
import redis.asyncio as redis
import asyncio
import json

STOPWORD = "STOP"
app = FastAPI()


async def get_redis_pubsub():
    r = await redis.from_url("redis://localhost:6379")
    return r.pubsub()

@app.websocket("/ws")
async def websocket_endpoint(channel: str, websocket: WebSocket):
    await websocket.accept()
    client_info = dict(websocket.headers)
    pubsub: redis.client.PubSub = await get_redis_pubsub()
    # 특정 채널 구독
    await pubsub.subscribe(channel)
    while True:
        try:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message is not None:
                decoded_msg = message["data"].decode()
                if decoded_msg == STOPWORD:
                    print("(Reader) STOP")
                    break
                print(decoded_msg)
                await websocket.send_text(decoded_msg)
        except Exception as e:
            print(e)
            await websocket.close()
            return
    await websocket.close()
    return
