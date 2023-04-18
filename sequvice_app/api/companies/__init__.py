from flask import request

from sequvice_app.models import Company


def check_auth(func):
    async def wrap(*args, **kwargs):
        auth_token = request.headers.get("Authorization")
        if not auth_token:
            return "Missing token.", 401

        if not auth_token.startswith("Bearer"):
            return "Wrong token scheme.", 401

        _, token = auth_token.split(" ")

        company = Company.load_from_token(token)
        if not company:
            return "Wrong token.", 401

        return await func(*args, **kwargs)

    return wrap
