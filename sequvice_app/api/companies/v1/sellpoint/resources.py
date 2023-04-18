from flask import request

from sequvice_app import app
from sequvice_app.models import SellPoint
from sequvice_app.api.companies import check_auth
from .schemas import SellPointData

ROOT_PATH = "/api/companies/v1/company/sellpoint"


@app.route(ROOT_PATH, methods=["POST"])
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
