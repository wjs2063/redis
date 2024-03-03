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
async def websocket_endpoint(channel: str, websocket: WebSocket):
    await websocket.accept()
    client_info = dict(websocket.headers)
    text = client_info.get("text")
    print(text)
    redis_reader: redis.client.PubSub = await get_redis_pubsub()
    # 특정 채널 구독
    await redis_reader.subscribe(channel)
    print(f"channel : {channel} 구독완료")
    # await call_external_server(channel, text)
    # 백그라운드 작업은 해당 엔드포인트의 핸들러함수가 종료되면 실행이된다. 따라서 직접 task 등록을 해주는것이 바로 요청을 보낼수있다.
    asyncio.create_task(call_external_server(channel, text))
    print(f"Background task 할당 완료, channel : {channel}, text : {text}")
    try:
        while True:
            message = await redis_reader.get_message(ignore_subscribe_messages=True)
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

