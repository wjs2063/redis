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
