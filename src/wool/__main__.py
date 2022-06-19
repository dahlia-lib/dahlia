from __future__ import annotations

from argparse import ArgumentParser
from sys import argv

from .wool import clean, config, test, wprint


def parse_args() -> tuple[str, bool]:
    UNSET = object()
    parser = ArgumentParser()
    parser.add_argument(
        "-d", "--depth", help="set the color depth", type=int, choices={3, 8, 24}
    )
    parser.add_argument(
        "-t", "--test", help="test the colors", action="store_true"
    )
    parser.add_argument(
        "-c", "--clean", help="clean codes", action="store_true"
    )
    parser.add_argument(
        "string", nargs="?", help="the string to color", default=UNSET
    )
    args = parser.parse_args()
    if args.depth is not None:
        config.depth = args.depth
    if args.string is UNSET:
        if args.test:
            test()
        exit()
    return args.string, args.clean


def main() -> None:
    string, clean_ = parse_args()
    if clean_:
        print(clean(string))
    else:
        wprint(string)


if __name__ == "__main__":
    main()
