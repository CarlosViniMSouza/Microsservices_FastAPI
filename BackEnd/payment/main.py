# external packages
from starlette.requests import Request
from redis_om import get_redis_connection, HashModel

# fastapi packages natives
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks

# packages python
import requests
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# This should be a different DB
redis = get_redis_connection(
    host="redis-*****.c239.us-east-1-2.ec2.cloud.redislabs.com",
    port="*****",
    password="*****",
    decode_response=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis


@app.get("/orders/{pk}")
def getOrder(pk: str):
    return Order.get(pk)


@app.post("/orders")
async def createOrder(request: Request, bgTasks: BackgroundTasks):
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2*product['price'],
        total=1.2*product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()

    bgTasks.add_task(orderCompleted, order)

    return order


def orderCompleted(order: Order):
    time.sleep(5)
    order.status = "completed"
    order.save()
