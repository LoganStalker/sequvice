import marshmallow as ma


class CustomersCompanyData(ma.Schema):
    name = ma.fields.String(required=True)
