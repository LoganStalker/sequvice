import marshmallow as ma
import phonenumbers


class CustomerRegistedData(ma.Schema):
    name = ma.fields.String(required=True)
    email = ma.fields.Email(required=False)
    phone = ma.fields.String(required=True)

    @ma.post_load
    def check_phone(self, data, **kwargs):
        phone = phonenumbers.parse(data["phone"])
        try:
            assert phonenumbers.is_valid_number(phone)
        except AssertionError:
            raise ma.exceptions.ValidationError("Invalid phone number.")

        return data
