import argparse

from sequvice_app import app


def make_args_parser():
    """Make parser for command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-run", required=False, action="store_true")
    parser.add_argument("-host", required=False, type=str)
    parser.add_argument("-port", required=False, type=int)

    return parser


if __name__ == "__main__":
    parser = make_args_parser()
    namespace = parser.parse_args()

    if namespace.run:
        HOST = namespace.host or "127.0.0.1"
        PORT = namespace.port or 5000
        app.run(host=HOST, port=PORT)
