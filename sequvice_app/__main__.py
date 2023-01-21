import asyncio
import argparse

from sequvice_app import db
from sequvice_app.models import Company, SellPoint, User, Order


def make_args_parser():
    """Make parser for command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-init_db", required=False, action="store_true")

    return parser


if __name__ == "__main__":
    parser = make_args_parser()
    namespace = parser.parse_args()

    if namespace.init_db:
        asyncio.run(db.create_tables())
