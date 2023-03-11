import marshmallow as ma


class CompanyRegisteredData(ma.Schema):
    name = ma.fields.String(required=True)
    email = ma.fields.Email(required=True)



