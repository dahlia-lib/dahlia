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

_ANSI_3BIT_PATTERN = r"\033\[(\d+)m"
_ANSI_8BIT_PATTERN = r"\033\[(?:3|4)8;5;(\d+)m"
_ANSI_24BIT_PATTERN = r"\033\[(?:3|4)8;2;(\d+);(\d+);(\d+)m"


class DahliaError(Exception):
    """An Exception for errors within Dahlia."""
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
            raise DahliaError(f"Invalid depth {value}, must be 3, 8, or 24")
        self._depth = value


config = _Config()


def _find_codes(string: str) -> list[tuple[str, bool, str]]:
    codes: list[tuple[str, bool, str]] = []
    for pattern in (_DEFAULT_PATTERN, _CUSTOM_PATTERN):
        for match in finditer(pattern, string):
            s, bg, color = (match.group(0), *match.groups())
            codes.append((s, bg == "~", color))
    return codes


def _find_ansi_codes(string: str) -> list[str]:
    return [
        match.group(0)
        for pattern in (_ANSI_3BIT_PATTERN, _ANSI_8BIT_PATTERN, _ANSI_24BIT_PATTERN)
        for match in finditer(pattern, string)
    ]


def _get_ansi(code: str, bg: bool = False) -> str:
    formats = _FORMAT_BG_TEMPLATES if bg else _FORMAT_TEMPLATES
    if len(code) == 6:
        template = formats[24]
        r, g, b = (int(code[i : i + 2], 16) for i in (0, 2, 4))
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
    """
    Removes all Dahlia formatting from a string.

    Parameters
    ----------
    string :
        String to clear formatting from.

    Returns
    -------
    str :
        Cleaned string without formatting.
    """
    for code, *_ in _find_codes(string):
        string = string.replace(code, "", 1)
    return string


def clean_ansi(string: str) -> str:
    """
    Removes all ANSI codes from a string.

    Parameters
    ----------
    string : str
        String to clear ANSI codes from.

    Returns
    -------
    str
        Cleaned string without codes.
    """
    for ansi_code in _find_ansi_codes(string):
        string = string.replace(ansi_code, "", 1)
    return string


def test() -> None:
    """Prints all default format codes and their formatting."""
    dprint("".join(f"&{i}{i}" for i in "0123456789abcdefg") + "&r&ll&r&mm&r&nn&r&oo")


def dahlia(string: str, *, no_reset: bool = False) -> str:
    """
    Formats a string using the format codes.

    Example
    -------

    .. code-block :: python

        text = dahlia("&aHello\\n&cWorld")
        print(text)


    Output would be 
    
    .. raw:: html
        
        <pre>
            <span class="&a">Hello</span>
            <span class="&c">World</span>
        </pre>

    For more see :ref:`dahlia usage <usage>`

    Parameters
    ----------
    string : str
        String containing text and format codes.
    no_reset : bool, default: False
        Whether ``&r`` should not be appended to the end of the string.
    
    Returns
    -------
    str
        A formatted string with the appropriate formatting applied.
    """
    if not (string.endswith("&r") or no_reset):
        string += "&r"
    for code, bg, color in _find_codes(string):
        string = string.replace(code, _get_ansi(color, bg))
    return string


def dinput(prompt: str, *, no_reset: bool = False) -> str:
    r""""
    Wrapper over :func:`input`, calling the :func:`dahlia` function on the prompt.

    Example
    -------
    .. code-block :: python

        text = dinput("&bEnter text: ")
    

    Output would be

    .. raw:: html

        <pre>
            <span class="&b">Enter text: </span>
        </pre>
    
    Parameters
    ----------
    prompt : str
        String containing text and format codes to prompt the user with.
    no_reset : bool, default: False
        Whether ``&r`` should not be appended to the end of the string.
    
    Returns
    -------
    str
        User input entered after the formatted prompt.
    """
    return input(dahlia(prompt, no_reset=no_reset))


def dprint(*string: str, **kwargs: Any) -> None:
    r"""
    Wrapper over :func:`print`, calling the :func:`dahlia` method for each argument.

    Example
    -------
    .. code-block :: python

        text = dprint("&bHello\n&5World")


    Output would be 
    
    .. raw:: html
        
        <pre>
            <span class="&b">Hello</span>
            <span class="&5">World</span>
        </pre>

    Parameters
    ----------
    \*string : str
        String(s) containing text and format codes.

    \*\*kwargs
        Keyword arguments to pass to :func:`print` and :func:`dahlia`.
    """
    no_reset = kwargs.pop("no_reset", False)
    print(*(dahlia(s, no_reset=no_reset) for s in string), **kwargs)


def reset() -> None:
    """Resets all modifiers. Equivalent to ``dprint("", end="")``."""
    dprint("", end="")
