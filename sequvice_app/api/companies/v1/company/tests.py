import asyncio

from sequvice_app.tests.helpers import autoflash
from sequvice_app.models import Company


@autoflash
async def test_first(app, client):
    loop = asyncio.get_running_loop()

    def sync_test():
        with client.get("/api/companies/v1/company/1") as res:
            assert res.status_code == 404
            json = res.json
            assert not json

        with client.post(
            "/api/companies/v1/company",
            json={"email": "Kus@Kus.ru", "name": "Pavel"}
        ) as res:
            assert res.status_code == 200
            json = res.json
            assert json

        with client.get("/api/companies/v1/company/1") as res:
            assert res.status_code == 200
            json = res.json
            assert json
            assert json == {"email": "Kus@Kus.ru", "name": "Pavel"}

    await loop.run_in_executor(None, sync_test)

    assert await Company.select().count() == 1
    company = await Company.select().first()
    assert company.id == 1
    assert company.name == "Pavel"
    assert company.email == "Kus@Kus.ru"
