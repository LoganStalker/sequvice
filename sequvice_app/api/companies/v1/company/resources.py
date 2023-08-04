from sequvice_app import app
from sequvice_app.models import Company
from sequvice_app.api.companies import check_auth
from .schemas import CompanyData

ROOT_PATH = "/api/companies/v1/company"


@app.route(f"{ROOT_PATH}", methods=["GET"])
@app.route(f"{ROOT_PATH}/<int:company_id>", methods=["GET"])
@check_auth
async def get_company(company: Company, *args, **kwargs):
    if company:
        return CompanyData().dump(company)
    return {}, 404
