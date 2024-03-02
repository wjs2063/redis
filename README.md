# redis
Redis(Pub-Sub Model)


![image](https://github.com/wjs2063/redis/assets/76778082/cb8988be-4c04-4849-b8fe-8f8475d58d1d)



## Usage 
Redis Server
Fastapi Server
Client Side code

```
# create redis server port 6379
docker compose up -d

# subscribe_server (fastapi)
uvicorn subscribe:app --host=0.0.0.0 --port=8000

# run publish code
python publish.py
```


Redis vs Kafka 

## Redis 
- subscribe 가 없다면 해당 channel(topic) 으로 전송된 데이터는 유실됨
- Redis Cluster 지원
- Redis sentinel 지원
- Inmemory 기반 ( 빠르지만 유실가능성 O, 영속성X)

## Kafka
- Topic - Partition 에 정보가 저장됨. 유실x
- 고가용성, Replica 지원
- Disk 기반 (Redis보다 상대적으로 느리지만 유실가능성이 현저히 적다)
- 
