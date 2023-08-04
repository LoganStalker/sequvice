import asyncio

from sequvice_app.tests.helpers import autoflash
from sequvice_app.models import Company


@autoflash
async def test_companies(app, client):
    loop = asyncio.get_running_loop()

    company = await Company.create(
        name="Company name",
        email="company1@gmail.com",
        password="PASSHASH"
    )
    await company.save()

    def sync_test():
        with client.get(f"/api/customers/v1/company/999") as res:
            assert res.status_code == 404
            json = res.json
            assert not json

        with client.get(f"/api/customers/v1/company/{company.id}") as res:
            assert res.status_code == 200
            json = res.json
            assert json
            assert "password" not in json
            assert "email" not in json
            assert "name" in json

        with client.get(f"/api/customers/v1/company") as res:
            assert res.status_code == 200
            json = res.json
            assert isinstance(json, list)

    await loop.run_in_executor(None, sync_test)
