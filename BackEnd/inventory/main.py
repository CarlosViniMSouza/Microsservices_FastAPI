from itertools import product
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

# This should be a different DB
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


def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.get("/")
async def root():
    return [format(pk) for pk in Product.all_pks()]


@app.get("/products/all")
async def getAllProducts():
    return Product.all_pks()


@app.get("/products/{pk}")
async def getProduct(pk: str):
    return Product.get(pk)


@app.post("/products")
def createProduct(product: Product):
    return product.save()


@app.post("/products/{pk}")
def createProduct(pk: str):
    return product.delete(pk)
