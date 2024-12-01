[![Dahlia spec](https://img.shields.io/badge/Dahlia%20spec-v1.0-pink?style=flat)](https://github.com/dahlia-lib/spec)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# Dahlia

Dahlia is a simple text formatting package, inspired by text formatting in the
game Minecraft.

## Installation

Dahlia is available on PyPI and can be installed with pip, or any other Python
package manager:
```console
$ pip install dahlia
```
(Some systems may require you to use `pip3`, `python -m pip`, or `py -m pip`
instead)

## [Documentation]

## Contributing
Contributions are welcome!

Please open an issue before submitting a pull request
(doesn't apply to minor changes like typos).

To get started:
1. Clone your fork of the project.
2. Install the project with [uv]:
```sh
uv sync
```
3. After you're done, use the following [`just`][just] recipes to check your
   changes (or run the commands manually):
```sh
just check     # pytest, mypy, ruff
just coverage  # pytest (with coverage), interrogate (docstring coverage)
```

## License

Dahlia is licensed under the MIT License.

If you have any questions, or would like to get in touch, join my
[Discord server]!

[Discord server]: https://discord.gg/C8QE5tVQEq
[Documentation]: https://dahlia-lib.github.io/dahlia/
[just]: https://github.com/casey/just
[uv]: https://docs.astral.sh/uv/
