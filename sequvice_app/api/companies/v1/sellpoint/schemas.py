import marshmallow as ma


class SellPointData(ma.Schema):
    name = ma.fields.String(required=True)
    logo = ma.fields.URL(required=False)
