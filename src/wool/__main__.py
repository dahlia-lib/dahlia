from argparse import ArgumentParser

from .wool import config, wprint


def parse_args() -> str:
    parser = ArgumentParser()
    parser.add_argument(
        "-s", "--section", help="Use § instead of & for wooling", action="store_true"
    )
    parser.add_argument(
        "-d", "--depth", help="Set the wool depth", type=int, choices={0, 8, 24}
    )
    parser.add_argument("string", help="The string to wool")
    args = parser.parse_args()
    config.char = "§" if args.section else "&"
    if args.depth is not None:
        config.depth = args.depth
    return args.string


def main() -> None:
    wprint(parse_args())


if __name__ == "__main__":
    main()
