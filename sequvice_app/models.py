import datetime as dt
import peewee as pw

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


@app.db.register
class SellPoint(BaseModel):
    name = pw.CharField(null=False)
    owner = pw.ForeignKeyField(Company, related_name="points")
    logo = pw.CharField(max_length=256, null=True)

    def __str__(self):
        return f"<SellPoint #{self.id}: {self.name}, owner #{self.owner}>"


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
