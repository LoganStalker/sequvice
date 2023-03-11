from flask import request

from sequvice_app import app
from sequvice_app.models import Company
from .schemas import CompanyRegisteredData

ROOT_PATH = "/api/companies/v1"
schema = CompanyRegisteredData()


@app.route(f"{ROOT_PATH}/company/<int:company_id>", methods=["GET"])
async def get_company(company_id=None):
    company = await Company.select().where(Company.id == company_id).first()
    if company:
        return schema.dump(company)
    return {}, 404


@app.route(f"{ROOT_PATH}/company", methods=["POST"])
async def create_company():
    data = request.get_json()
    data = schema.load(data)

    company = await Company.select().where(Company.email == data["email"]).first()

    if not company:
        company = await Company.create(**data)

    return schema.dump(company)
