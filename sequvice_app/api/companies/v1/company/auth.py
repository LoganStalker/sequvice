from flask import request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from sequvice_app import app
from sequvice_app.models import Company
from .schemas import CompanyRegisteredData, CompanyLoginData

ROOT_PATH = "/api/companies/v1/company/auth"


@app.route(f"{ROOT_PATH}/register", methods=["POST"])
async def company_auth():
    """Create company if not exist and redirect to login."""  # noqa
    data = request.get_json()
    data = CompanyRegisteredData().load(data)

    if await Company.select().where(Company.email == data["email"]).exists():
        return redirect(url_for("company_login"))

    data["password"] = generate_password_hash(data["password"])
    await Company.create(**data)

    return redirect(url_for("company_login"))


@app.route(f"{ROOT_PATH}/login", methods=["POST"])
async def company_login():
    """Check login and password and retrun auth token."""
    data = request.get_json()
    data = CompanyLoginData().load(data)
    company = await Company.select().where(Company.email == data["email"]).first()
    if not company:
        return {}, 404

    password_hash = generate_password_hash(data["password"])
    if not check_password_hash(password_hash, company.password):
        return {}, 401

    return {"token": company.token}
