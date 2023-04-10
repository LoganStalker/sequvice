import asyncio
import argparse
from peewee_migrate import Router

from sequvice_app import app
from sequvice_app.models import Company, SellPoint, Customer, Order


def make_args_parser():
    """Make parser for command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-create", required=False, action="store_true")
    parser.add_argument("-migrate", required=False, action="store_true")
    parser.add_argument("-rollback", required=False, action="store_true")
    parser.add_argument("-name", required=False, type=str)

    return parser


if __name__ == "__main__":
    parser = make_args_parser()
    namespace = parser.parse_args()

    router = Router(app.db.pw_database, migrate_dir="migrations")

    if namespace.create:
        with app.db.allow_sync():
            router.create(namespace.name or None, auto=list(app.db.models))

    if namespace.migrate:
        with app.db.allow_sync():
            router.run()

    if namespace.rollback:
        with app.db.allow_sync():
            router.rollback()
