from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel

app = FastAPI()

redis = get_redis_connection(
    host="redis-*****.c239.us-east-1-2.ec2.cloud.redislabs.com",
    port="*****",
    password="*****",
    decode_response=True
)


class Product(HashModel):
    name: str
    price: float
    quant: int

    class Meta:
        database = redis


@app.get("/")
async def root():
    return {"data": "message"}
