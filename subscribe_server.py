from fastapi import FastAPI, Depends, WebSocket, BackgroundTasks
import async_timeout
import redis.asyncio as redis
import httpx
import asyncio
import json

STOPWORD = "STOP"
app = FastAPI()


async def get_redis_pubsub():
    r = await redis.from_url("redis://localhost:6379")
    return r.pubsub()


async def call_external_server(channel, text):
    print("call_external_server start")
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:9000/pub?channel={channel}&text={text}", )  # 외부 서버의 URL로 변경
    print("call_external_server finished")
    return {"response": "external_server is done"}


@app.websocket("/ws")
async def websocket_endpoint(channel: str, websocket: WebSocket, background_task: BackgroundTasks):
    await websocket.accept()
    client_info = dict(websocket.headers)
    text = client_info.get("text")
    pubsub: redis.client.PubSub = await get_redis_pubsub()
    # 특정 채널 구독
    await pubsub.subscribe(channel)
    background_task.add_task(call_external_server, channel=channel, text=text)
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
