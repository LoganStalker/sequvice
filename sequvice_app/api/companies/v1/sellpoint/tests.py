import asyncio

from sequvice_app.tests.helpers import autoflash
from sequvice_app.models import Company


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
    assert company.name == "Pavel"
    assert await company.points.count() == 1

    sellpoint = await company.points.get()
    assert sellpoint.id == 1
    assert sellpoint.name == "Варгаш Пахилий"
    assert sellpoint.logo == "https://vk.com/pahilij_avatar"
    assert await sellpoint.owner == company
