import asyncio

import pytest
from unittest import mock


@pytest.fixture(scope='session')
def app():
    from sequvice_app import app

    yield app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def runner(app):
    return app.test_cli_runner()
