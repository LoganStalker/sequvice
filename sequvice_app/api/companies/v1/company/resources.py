from flask import request

from sequvice_app import app
from sequvice_app.models import Company, SellPoint
from sequvice_app.api.companies import check_auth
from .schemas import CompanyData, SellPointData

ROOT_PATH = "/api/companies/v1/company"


@app.route(f"{ROOT_PATH}", methods=["GET"])
@app.route(f"{ROOT_PATH}/<int:company_id>", methods=["GET"])
@check_auth
async def get_company(company, *args, **kwargs):
    company = await Company.select().where(Company.id == company.id).first()
    if company:
        return CompanyData().dump(company)
    return {}, 404


@app.route(f"{ROOT_PATH}/sellpoint", methods=["POST"])
@check_auth
async def create_sell_point(company):
    data = request.get_json()
    schema = SellPointData()
    data = schema.load(data)

    sellpoint = await SellPoint.select().where(
        SellPoint.name == data["name"],
        SellPoint.owner == company
    ).first()

    if not sellpoint:
        data["owner"] = company
        sellpoint = await SellPoint.create(**data)

    return schema.dump(sellpoint)
