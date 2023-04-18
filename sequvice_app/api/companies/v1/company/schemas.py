import marshmallow as ma


class CompanyData(ma.Schema):
    name = ma.fields.String(required=True)
    email = ma.fields.Email(required=True)


class CompanyRegisteredData(CompanyData):
    password = ma.fields.String(required=True, load_only=True)


class CompanyLoginData(ma.Schema):
    email = ma.fields.Email(required=True)
    password = ma.fields.String(required=True, load_only=True)


class SellPointData(ma.Schema):
    name = ma.fields.String(required=True)
    logo = ma.fields.URL(required=False)
