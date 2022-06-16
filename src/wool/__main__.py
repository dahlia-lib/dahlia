from argparse import ArgumentParser

from .wool import config, wprint


def parse_args() -> str:
    parser = ArgumentParser()
    parser.add_argument(
        "-d", "--depth", help="Set the wool depth", type=int, choices={3, 8, 24}
    )
    parser.add_argument("string", help="The string to wool")
    args = parser.parse_args()
    if args.depth is not None:
        config.depth = args.depth
    return args.string


def main() -> None:
    wprint(parse_args())


if __name__ == "__main__":
    main()
