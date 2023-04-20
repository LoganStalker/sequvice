"""Peewee migrations -- 001_initinal.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import peewee as pw
from peewee_migrate import Migrator
from decimal import ROUND_HALF_EVEN

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    
    @migrator.create_model
    class Company(pw.Model):
        id = pw.AutoField()
        created = pw.DateTimeField()
        name = pw.CharField(max_length=255)
        email = pw.CharField(max_length=255, unique=True)

        class Meta:
            table_name = "company"

    @migrator.create_model
    class Customer(pw.Model):
        id = pw.AutoField()
        created = pw.DateTimeField()
        name = pw.CharField(max_length=255, null=True)
        email = pw.CharField(max_length=255, null=True, unique=True)
        phone = pw.CharField(max_length=255, unique=True)

        class Meta:
            table_name = "customer"

    @migrator.create_model
    class SellPoint(pw.Model):
        id = pw.AutoField()
        created = pw.DateTimeField()
        name = pw.CharField(max_length=255)
        logo = pw.CharField(max_length=256, null=True)
        owner = pw.ForeignKeyField(column_name='owner_id', field='id', model=migrator.orm['company'])

        class Meta:
            table_name = "sellpoint"

    @migrator.create_model
    class Order(pw.Model):
        id = pw.AutoField()
        created = pw.DateTimeField()
        description = pw.TextField(null=True)
        status = pw.CharField(constraints=[SQL("DEFAULT 'new'")], default='new', max_length=255)
        sell_point = pw.ForeignKeyField(column_name='sell_point_id', field='id', model=migrator.orm['sellpoint'])
        customer = pw.ForeignKeyField(column_name='customer_id', field='id', model=migrator.orm['customer'])

        class Meta:
            table_name = "order"


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.remove_model('order')

    migrator.remove_model('sellpoint')

    migrator.remove_model('customer')

    migrator.remove_model('company')
