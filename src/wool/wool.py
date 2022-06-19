from __future__ import annotations

import json
import os

from dataclasses import dataclass
from re import finditer
from sys import platform
from typing import Any


if platform in {"win32", "cygwin"}:
    os.system("")


with open(f"{os.path.dirname(__file__)}/codes.json") as f:
    _CODES = json.load(f)


_FORMAT_TEMPLATES = {3: "\033[{}m", 8: "\033[38;5;{}m", 24: "\033[38;2;{};{};{}m"}
_FORMAT_BG_TEMPLATES = {3: "\033[{}m", 8: "\033[48;5;{}m", 24: "\033[48;2;{};{};{}m"}

_STYLE_CODES = "lmnor"

_DEFAULT_PATTERN = r"&(~?)([0-9a-gl-or])"
_CUSTOM_PATTERN = r"&(~?)\[#([0-9a-fA-F]{6})\]"


class WoolError(Exception):
    pass


@dataclass
class _Config:
    _depth: int = 24

    def __repr__(self) -> str:
        return f"Config[{self.depth}]"

    @property
    def depth(self) -> int:
        return self._depth

    @depth.setter
    def depth(self, value: int) -> None:
        if value not in {3, 8, 24}:
            raise WoolError(f"Invalid depth {value}, must be 3, 8, or 24")
        self._depth = value


config = _Config()


def _find_codes(string: str) -> list[tuple[str, bool, str]]:
    codes: list[tuple[str, bool, str]] = []
    for pattern in (_DEFAULT_PATTERN, _CUSTOM_PATTERN):
        for match in finditer(pattern, string):
            s, bg, color = (match.group(0), *match.groups())
            codes.append((s, bg == "~", color))
    return codes


def _get_ansi(code: str, bg: bool = False) -> str:
    formats = _FORMAT_BG_TEMPLATES if bg else _FORMAT_TEMPLATES
    if len(code) == 6:
        template = formats[24]
        r, g, b = (int(code[i:i + 2], 16) for i in (0, 2, 4))
        return template.format(r, g, b)
    else:
        if code in _STYLE_CODES:
            template = formats[3]
            value = _CODES["format"][code]
        else:
            template = formats[config.depth]
            value = _CODES[str(config.depth)][code]
        if config.depth == 8 or code in _STYLE_CODES:
            return template.format(value)
        elif config.depth == 24:
            return template.format(*value)
        else:
            return template.format(value + 10 * bg)


def clean(string: str) -> str:
    for code, *_ in _find_codes(string):
        string = string.replace(code, "", 1)
    return string


def test():
    wprint("".join(f"&{i}{i}" for i in "0123456789abcdefg") + "&r&ll&r&mm&r&nn&r&oo")


def wool(string: str) -> str:
    if not string.endswith("&r"):
        string += "&r"
    for code, bg, color in _find_codes(string):
        string = string.replace(code, _get_ansi(color, bg))
    return string


def wprint(*string: str, **kwargs: Any) -> None:
    print(*map(wool, string), **kwargs)
