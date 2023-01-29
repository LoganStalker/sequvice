from flask import request

from sequvice_app import app
from sequvice_app.models import Customer
from .schemas import CustomerRegistedData


ROOT_PATH = "/api/customers/v1"
schema = CustomerRegistedData()


@app.route(f"{ROOT_PATH}/customer/<int:customer_id>", methods=["GET"])
async def get_customer(customer_id=None):
    customer = await Customer.select().where(Customer.id == customer_id).first()
    if customer:
        return schema.dump(customer)
    return {}, 404


@app.route(f"{ROOT_PATH}/customer", methods=["POST"])
async def create_customer():
    data = request.get_json()
    data = schema.load(data)

    customer = await Customer.select().where(Customer.phone == data["phone"]).first()

    if not customer:
        customer = await Customer.create(**data)

    return schema.dump(customer)
