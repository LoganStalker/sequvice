import asyncio

from sequvice_app.tests.helpers import autoflash
from sequvice_app.models import Company, SellPoint


@autoflash
async def test_companies(app, client):
    loop = asyncio.get_running_loop()

    def sync_test():
        # try to get not existing company
        with client.get("/api/companies/v1/company/1") as res:
            assert res.status_code == 401
            json = res.json
            assert not json

        # register company (create new account)
        with client.post(
            "/api/companies/v1/company/auth/register",
            json={"name": "Pavel", "email": "Kus@Kus.ru", "password": "MyPass"}
        ) as res:
            assert res.status_code == 302
            assert res.location.endswith("/login")

        # try to get existing company withot login
        with client.get("/api/companies/v1/company/1") as res:
            assert res.status_code == 401
            assert res.text == "Missing token."

        # try to get existing company with not Bearer token
        with client.get(
            "/api/companies/v1/company/1",
            headers={"Authorization": "asdfasdasd"}
        ) as res:
            assert res.status_code == 401
            assert res.text == "Wrong token scheme."

        # try to get existing company with wrong Bearer token
        with client.get(
            "/api/companies/v1/company/1",
            headers={"Authorization": "Bearer asdfasdasd"}
        ) as res:
            assert res.status_code == 401
            assert res.text == "Wrong token."

        # try login and get token
        with client.post(
            "/api/companies/v1/company/auth/login",
            json={"email": "Kus@Kus.ru", "password": "MyPass"}
        ) as res:
            assert res.status_code == 200
            json = res.get_json()
            assert json
            token = json["token"]
            assert token

        auth = {"Authorization": f"Bearer {token}"}
        with client.get(
            "/api/companies/v1/company/1",
            headers=auth
        ) as res:
            assert res.status_code == 200
            json = res.json
            assert json
            assert json == {"name": "Pavel", "email": "Kus@Kus.ru"}

    await loop.run_in_executor(None, sync_test)

    assert await Company.select().count() == 1
    company = await Company.select().first()
    assert company.id == 1
    assert company.name == "Pavel"
    assert company.email == "Kus@Kus.ru"


@autoflash
async def test_creating_sellpoint(app, client):
    loop = asyncio.get_running_loop()

    def sync_test():
        # register company (create new account)
        with client.post(
            "/api/companies/v1/company/auth/register",
            json={"name": "Pavel", "email": "Kus@Kus.ru", "password": "MyPass"}
        ) as res:
            assert res.status_code == 302

        # try login and get token
        with client.post(
            "/api/companies/v1/company/auth/login",
            json={"email": "Kus@Kus.ru", "password": "MyPass"}
        ) as res:
            assert res.status_code == 200
            json = res.get_json()
            token = json["token"]

        # create new sellpoint
        datas = {
            "name": "Варгаш Пахилий",
            "logo": "https://vk.com/pahilij_avatar"
        }
        auth = {"Authorization": f"Bearer {token}"}
        with client.post(
            "/api/companies/v1/company/sellpoint",
            headers=auth,
            json=datas
        ) as res:
            assert res.status_code == 200
            json = res.json
            assert json
            assert json == datas

    await loop.run_in_executor(None, sync_test)

    assert await Company.select().count() == 1
    company = await Company.select().first()
    assert company.id == 1
    assert company.name == "Pavel"
    assert company.email == "Kus@Kus.ru"
    assert await company.points.count() == 1

    assert await SellPoint.select().count() == 1
    sellpoint = await SellPoint.get()
    assert sellpoint.id == 1
    assert sellpoint.name == "Варгаш Пахилий"
    assert sellpoint.logo == "https://vk.com/pahilij_avatar"
    assert await sellpoint.owner == company
