from __future__ import annotations

from abc import ABC, abstractmethod
from math import dist
from re import Match, Pattern, compile
from typing import Literal

from .constants import ANSI_COLOR_REGEX, ANSI_REGEXES, CODE_REGEXES, COLORS_3, COLORS_4


def clean(string: str, marker: str = "&") -> str:
    """
    Removes all Dahlia formatting from a string.

    Parameters
    ----------
    string : str
        String to clear formatting from.

    marker : str
        Specifies the prefix used by format codes ("&" by default)

    Returns
    -------
    str :
        Cleaned string without formatting.
    """
    for code, *_ in _find_codes(string, _with_marker(marker)):
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


def _find_codes(string: str, patterns: list[Pattern]) -> list[tuple[str, bool, str]]:
    codes: list[tuple[str, bool, str]] = []
    for pattern in patterns:
        for match in pattern.finditer(string):
            codes.append((match[0], match[1] == "~", match[2]))
    return codes


def _find_ansi_codes(string: str) -> list[str]:
    ansi_codes: list[str] = []
    for pattern in ANSI_REGEXES:
        for match in pattern.finditer(string):
            ansi_codes.append(match.group(0))
    return ansi_codes


def _with_marker(marker: str) -> list[Pattern]:
    if len(marker) != 1:
        raise ValueError("The marker has to be a single character")
    return [compile(marker + i) for i in CODE_REGEXES]


def _quantize_8_bit(ansi_code: int, to: Literal[3, 4]) -> tuple[int, int, int] | int:
    if 0 <= ansi_code <= 7:
        return 30 + ansi_code

    if 8 <= ansi_code <= 15:
        return (90 if to == 4 else 30) + ansi_code - 8

    if 232 <= ansi_code <= 255:
        step = int(float(255 / 24) * (255 - ansi_code))
        return (step, step, step)

    n = ansi_code - 16

    g = (n % 36) // 6
    b = n % 6
    r = (n - g - b) // 36

    return (r * 51, g * 51, b * 51)


def _estimate_ansi_color(
    rgb: tuple[int, int, int],
    colors: dict[tuple[int, int, int], int],
    *,
    background: bool,
) -> str:
    closest = min(colors.keys(), key=lambda x: dist(rgb, x))
    num = colors[closest]
    if background:
        num += 10
    return f"\x1b[{num}m"


class _ANSI(ABC):
    @abstractmethod
    def __init__(self, ansi: list[str], old_ansi: list[str]) -> None:
        ...

    @abstractmethod
    def to_3(self) -> str:
        ...

    @abstractmethod
    def to_4(self) -> str:
        ...

    @abstractmethod
    def to_8(self) -> str:
        ...


class _ANSI3(_ANSI):
    def __init__(self, _ansi: list[str], old_ansi: str) -> None:
        self.old_ansi = old_ansi

    def to_3(self) -> str:
        return self.old_ansi

    def to_4(self) -> str:
        return self.old_ansi

    def to_8(self) -> str:
        return self.old_ansi


class _ANSI4(_ANSI):
    def __init__(self, ansi: list[str], old_ansi: str) -> None:
        if ansi[0] == 1:
            self.bold = True
            color = int(ansi[1])
        else:
            color = int(ansi[0])

        self.color = color % 10

        if 40 <= color <= 47 or 100 <= color <= 107:
            self.background = True

        self.old_ansi = old_ansi

    def to_3(self) -> str:
        color = self.color + 30

        if self.background:
            color += 10

        if self.bold:
            return f"\x1b[1;{color}m"

        return f"\x1b[{color}m"

    def to_4(self) -> str:
        return self.old_ansi

    def to_8(self) -> str:
        return self.old_ansi


class _ANSI8(_ANSI):
    def __init__(self, ansi: list[str], old_ansi: str) -> None:
        self.color = int(ansi[2])
        self.background = ansi[0] == "48"
        self.old_ansi = old_ansi

    def to_3(self) -> str:
        eight = _quantize_8_bit(self.color, to=3)

        if isinstance(eight, int):
            return f"\x1b[{eight + (10 if self.background else 0)}m"
        
        return _estimate_ansi_color(eight, COLORS_3, background=self.background)

    def to_4(self) -> str:
        eight = _quantize_8_bit(self.color, to=4)

        if isinstance(eight, int):
            return f"\x1b[{eight + (10 if self.background else 0)}m"

        return _estimate_ansi_color(eight, COLORS_4, background=self.background)

    def to_8(self) -> str:
        return self.old_ansi


class _ANSI24(_ANSI):
    def __init__(self, ansi: list[str], _old_ansi: str) -> None:
        self.rgb = (int(ansi[2]), int(ansi[3]), int(ansi[4]))
        self.background = ansi[0] == "48"

    def to_3(self) -> str:
        return _estimate_ansi_color(self.rgb, COLORS_3, background=self.background)

    def to_4(self) -> str:
        return _estimate_ansi_color(self.rgb, COLORS_4, background=self.background)

    def to_8(self) -> str:
        r, g, b = self.rgb

        color = 36 * (r // 51) + 6 * (g // 51) + (b // 51)

        return f"\x1b[{48 if self.background else 38};5;{color + 16}m"


def _build_ansi(old_ansi: str) -> _ANSI:
    ansi = old_ansi.split(";")

    ansi[0] = ansi[0].removeprefix("\x1b[")
    ansi[-1] = ansi[-1].removesuffix("m")

    if len(ansi) < 3:
        color = int(ansi[1] if ansi[0] == 1 else ansi[0])

        if color < 90:
            return _ANSI3(ansi, old_ansi)
        else:
            return _ANSI4(ansi, old_ansi)

    if ansi[1] == "5":
        return _ANSI8(ansi, old_ansi)

    if ansi[1] == "2":
        return _ANSI24(ansi, old_ansi)

    raise NotImplementedError(
        "There should never be an ANSI code that does not follow these rules."
    )


def quantize_ansi(string: str, *, to: Literal[3, 4, 8]) -> str:
    """
    Quantize the ANSI codes in a string to ANSI codes with of a lower amount of
    bits.

    Parameters
    ----------
    string : str
        String to quantize ANSI in.

    to : int
        The amount of bits to convert to.

    Returns
    -------
    str :
        String with quantized ANSI.
    """

    def replace_color(match: Match[str]) -> str:
        m = match.group()
        ansi_ = _build_ansi(m)
        if to == 3:
            return ansi_.to_3()
        if to == 4:
            return ansi_.to_4()

        return ansi_.to_8()

    return ANSI_COLOR_REGEX.sub(replace_color, string)
