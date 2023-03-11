import asyncio

from sequvice_app.tests.helpers import autoflash
from sequvice_app.models import Customer


@autoflash
async def test_first(app, client):
    loop = asyncio.get_running_loop()

    def sync_test():
        with client.get("/api/customers/v1/customer/1") as res:
            assert res.status_code == 404
            json = res.json
            assert not json

        with client.post(
            "/api/customers/v1/customer",
            json={"name": "Eugene", "phone": "+79991112233"}
        ) as res:
            assert res.status_code == 200
            json = res.json
            assert json

        with client.get("/api/customers/v1/customer/1") as res:
            assert res.status_code == 200
            json = res.json
            assert json
            assert json == {"email": None, "name": "Eugene", "phone": "+79991112233"}

    await loop.run_in_executor(None, sync_test)

    assert await Customer.select().count() == 1

    customer = await Customer.select().first()
    assert customer.id == 1
    assert customer.name == "Eugene"
    assert not customer.email
    assert customer.phone == "+79991112233"
