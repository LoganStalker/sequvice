import asyncio
import argparse

from sequvice_app import app
from sequvice_app.models import Company, SellPoint, Customer, Order


def make_args_parser():
    """Make parser for command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-init_db", required=False, action="store_true")
    parser.add_argument("-run", required=False, action="store_true")
    parser.add_argument("-host", required=False, type=str)
    parser.add_argument("-port", required=False, type=int)

    return parser


if __name__ == "__main__":
    parser = make_args_parser()
    namespace = parser.parse_args()

    if namespace.init_db:
        asyncio.run(app.db.create_tables())

    if namespace.run:
        HOST = namespace.host or "127.0.0.1"
        PORT = namespace.port or 5000
        app.run(host=HOST, port=PORT)
