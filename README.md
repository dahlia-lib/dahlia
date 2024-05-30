[![Dahlia spec](https://img.shields.io/badge/Dahlia%20spec-v1.0-pink?style=flat)](https://github.com/dahlia-lib/spec)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# Dahlia

Dahlia is a simple text formatting package, inspired by text formatting in the
game Minecraft.

Text is formatted in a similar way to in the game. With Dahlia, it is formatted
by typing a special character `&` followed by a format code and finally the text
to be formatted.

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

Please open an issue before submitting a pull request (unless it's a minor
change like fixing a typo).

To get started:
1. Clone your fork of the project.
2. Set up the project with `just install` (make sure you have [poetry]
   installed).
3. After you're done, run `just check` to check your changes.

> [!Note]
> If you don't want to install [just], simply look up the recipes
> in the project's [`justfile`][justfile].


## License

Dahlia is licensed under the MIT License.

[Documentation]: https://dahlia-lib.github.io/dahlia/
[just]: https://github.com/casey/just
[justfile]: https://github.com/dahlia-lib/dahlia/blob/master/justfile
[poetry]: https://python-poetry.org/
