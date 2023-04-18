import asyncio

from sequvice_app.tests.helpers import autoflash
from sequvice_app.models import Company


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
