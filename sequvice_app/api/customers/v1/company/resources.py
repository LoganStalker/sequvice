from sequvice_app import app
from sequvice_app.models import Company
from .schemas import CustomersCompanyData

ROOT_PATH = "/api/customers/v1"
schema = CustomersCompanyData()


@app.route(f"{ROOT_PATH}/company/<int:company_id>", methods=["GET"])
async def get_company_for_customers(company_id=None):
    company = await Company.select().where(Company.id == company_id).first()
    if company:
        return schema.dump(company)
    return {}, 404
