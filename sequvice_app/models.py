import datetime as dt
import peewee as pw
import jwt

from sequvice_app import app
from sequvice_app.utils import Choices


class BaseModel(app.db.Model):
    created = pw.DateTimeField(default=dt.datetime.utcnow)

    @property
    def pk(self):
        return self.get_id()


@app.db.register
class Company(BaseModel):
    name = pw.CharField(null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=True)

    def __str__(self):
        return f"<Company: {self.name}>"

    @property
    def token(self):
        return jwt.encode(
            {
                "id": self.id,
                "email": self.email,
                "exp": dt.datetime.utcnow() + dt.timedelta(seconds=3600*24*30),
            },
            app.cfg.TOKEN_SECRET,
        )

    @classmethod
    async def load_from_token(cls, token):
        """Load customer from token."""
        try:
            payload = jwt.decode(token, app.cfg.TOKEN_SECRET, algorithms=["HS256"])
            company = await cls.select().where(cls.id == payload["id"]).first()
            return company
        # TODO: add except for non exist company
        except (jwt.InvalidTokenError, KeyError):
            return None


@app.db.register
class SellPoint(BaseModel):
    name = pw.CharField(null=False)
    owner = pw.ForeignKeyField(Company, related_name="points")
    logo = pw.CharField(max_length=256, null=True)
    active = pw.BooleanField(default=True)
    address = pw.CharField(null=False)
    email = pw.CharField(null=False)
    password = pw.CharField(null=False)

    def __str__(self):
        return f"<SellPoint #{self.id}: {self.name}, owner #{self.owner}>"

    @property
    def token(self):
        return jwt.encode(
            {
                "id": self.id,
                "email": self.email,
                "exp": dt.datetime.utcnow() + dt.timedelta(seconds=3600 * 24 * 30),
            },
            app.cfg.TOKEN_SECRET,
        )

    @classmethod
    async def load_from_token(cls, token):
        """Load customer from token."""
        try:
            payload = jwt.decode(token, app.cfg.TOKEN_SECRET, algorithms=["HS256"])
            sp = await cls.select().where(cls.id == payload["id"]).first()
            return sp
        # TODO: add except for non exist company
        except (jwt.InvalidTokenError, KeyError):
            return None


@app.db.register
class Customer(BaseModel):
    name = pw.CharField(null=True)
    email = pw.CharField(unique=True, null=True)
    phone = pw.CharField(unique=True, null=False)

    def __str__(self):
        return f"<User: {self.id}>"


@app.db.register
class Order(BaseModel):
    STATUSES = Choices("new", "in progress", "packed", "done")

    description = pw.TextField(null=True)
    status = pw.CharField(null=False, default=STATUSES.new)
    sell_point = pw.ForeignKeyField(SellPoint, related_name="orders")
    customer = pw.ForeignKeyField(Customer, related_name="orders")

    def __str__(self):
        return f"<Order: {self.id}>"
