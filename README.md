# redis
Redis(Pub-Sub Model)


![image](https://github.com/wjs2063/redis/assets/76778082/b1d46358-a957-401f-8010-2a68b4c692f1)


### 시나리오 
```
1. 클라이언트와 subscribe서버 와 웹소켓 연동 
2. subcribe 서버는 channel 구독후(필수) 특정채널을 수신 대기 
3. BackgroundTask로 publish 서버로 text 를 담아 요청
4. Publish 서버는 비즈니스로직수행후 데이터를 Redis 특정 channel 로 발행한다.
5. subscribe 서버는 데이터를 지속적으로 받는다 (STOP 받을시 종료)
6. 클라이언트는 웹소켓을통해 실시간으로 데이터를 받는다.
```

### Why Pub/Sub model?? 

설계의 주요 포인트중하나인 결합도를 낮추고 응집력을 높이는것이 중요하다.
서버들간의 결합도를 낮춘다.  즉 Decoupling 시킴으로써 서버확장을 유연하게 가져갈수있다. 




## Usage 
Redis Server
Fastapi Server
Client Side code

```
# create redis server port 6379
docker compose up -d

# 이순서로 서버 구동

# subscribe_server (fastapi)
uvicorn subscribe:app --host=0.0.0.0 --port=8000

# run publish code
uvicorn main:app --host=0.0.0.0 --port=9000

# run client_server
python client_server.py


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
