from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

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


@app.get("/products/all")
async def allProducts():
    return Product.all_pks()
