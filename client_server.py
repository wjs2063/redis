import asyncio

import redis.asyncio as redis
import websockets


async def pub_redis(vin):
    r = redis.from_url("redis://localhost:6379")

    await r.publish(vin, "test_example")


async def connect_websocket():
    ws = await websockets.connect("ws://localhost:8000/ws?channel=1234", extra_headers={"channel": "1234"})
    try:
        while True:
            data = await ws.recv()
            print(data)
    except Exception as e:
        print(e)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(asyncio.gather(connect_websocket()))
