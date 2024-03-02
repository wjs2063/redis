import asyncio
import datetime

import redis.asyncio as redis


async def publish(channel):
    r = redis.from_url("redis://localhost:6379")
    idx = 0
    try:
        while idx < 10:
            await r.publish(channel, f"test_example:{datetime.datetime.now()}")
            await asyncio.sleep(1)
            idx += 1
    except Exception as e:
        print(e)
    await r.publish(channel, "STOP")


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(asyncio.gather(publish("1234")))
