from __future__ import annotations

from argparse import ArgumentParser

from .dahlia import clean, clean_ansi, config, test, dprint


def parse_args() -> tuple[str, bool, bool]:
    UNSET = object()
    parser = ArgumentParser()
    parser.add_argument(
        "-d", "--depth", help="set the color depth", type=int, choices={3, 8, 24}
    )
    parser.add_argument(
        "-t", "--test", help="test the colors", action="store_true"
    )
    parser.add_argument(
        "-v", "--version", help="print the version", action="store_true"
    )
    parser.add_argument(
        "-c", "--clean", help="clean codes", action="store_true"
    )
    parser.add_argument(
        "-a", "--clean-ansi", help="clean ANSI codes", action="store_true"
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
        elif args.version:
            print("Dahlia 1.0.0")
        exit()
    return args.string, args.clean, args.clean_ansi


def main() -> None:
    string, clean_, clean_ansi_ = parse_args()
    if clean_:
        print(clean(string))
    elif clean_ansi_:
        print(clean_ansi(string))
    else:
        dprint(string)


if __name__ == "__main__":
    main()
