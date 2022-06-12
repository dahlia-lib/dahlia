from __future__ import annotations

import json
import os

from dataclasses import dataclass
from typing import Any
from sys import platform


if platform in {"win32", "cygwin"}:
    os.system("")


with open(f"{os.path.dirname(__file__)}/codes.json") as f:
    __CODES = json.load(f)


__FORMAT_TEMPLATES = {0: "\033[{}m", 8: "\033[38;5;{}m", 24: "\033[38;2;{};{};{}m"}

__STYLE_CODES = "lmnor"


class WoolError(Exception):
    pass


AMPERSAND = "&"
SECTION_SIGN = "§"


@dataclass
class __Config:
    __char: str = "&"
    __depth: int = 24

    def __repr__(self) -> str:
        return f"Config[{self.char} | {self.depth}]"

    @property
    def depth(self) -> int:
        return self.__depth
    
    @depth.setter
    def depth(self, value: int) -> None:
        if value not in {0, 8, 24}:
            raise WoolError(f"Invalid depth {value}, must be 0, 8, or 24")
        self.__depth = value

    @property
    def char(self) -> str:
        return self.__char

    @char.setter
    def char(self, value: str) -> None:
        if value not in "&§":
            raise WoolError(f"Invalid character '{value}', must be '&' or '§'")
        self.__char = value


config = __Config()


def __get_ansi(char: str) -> str:
    if char in __STYLE_CODES:
        filler = __CODES["format"][char]
        template = __FORMAT_TEMPLATES[0]
    else:
        filler = __CODES[str(config.depth)][char]
        template = __FORMAT_TEMPLATES[config.depth]
    if config.depth == 24 and char not in __STYLE_CODES:
        return template.format(*filler)
    return template.format(filler)


def test():
    wprint("&00&11&22&33&44&55&66&77&88&99&aa&bb&cc&dd&ee&ff&gg&r&ll&r&mm&r&nn&r&oo")


def wool(string: str) -> str:
    prefix = config.char
    if string[-2:] not in {"&r", "§r"}:
        string += config.char + "r"
    for char in "0123456789abcdefglmnor":
        if (code := prefix + char) in string:
            string = string.replace(code, __get_ansi(char))
    return string


def wprint(*string: str, **kwargs: Any) -> None:
    print(*map(wool, string), **kwargs)
