from re import Pattern, compile, Match
from typing import Literal
from math import dist

from .constants import ANSI_REGEXES, CODE_REGEXES


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


ANSI_REGEX = compile(
    r"\033\[(?:(3[0-7]|[012][0-7])|4(?:[0-7]|8[0-5])|38;5;([0-9]+)|38;2;(\d+;\d+;\d+))m"
)


COLORS_3 = {
    (0, 0, 0): 30,  # black
    (128, 0, 0): 31,  # dark red
    (0, 128, 0): 32,  # dark green
    (128, 128, 0): 33,  # dark yellow
    (0, 0, 128): 34,  # dark blue
    (128, 0, 128): 35,  # dark magenta
    (0, 128, 128): 36,  # dark cyan
    (192, 192, 192): 37,  # light gray
    (128, 128, 128): 30,  # dark gray

    # Birght colors are added and linked to the darker ones to improve results.
    (128, 128, 128): 30,  # dark gray
    (255, 0, 0): 31,  # bright red
    (0, 255, 0): 32,  # bright green
    (255, 255, 0): 33,  # bright yellow
    (0, 0, 255): 34,  # bright blue
    (255, 0, 255): 35,  # bright magenta
    (0, 255, 255): 36,  # bright cyan
    (255, 255, 255): 37,  # white
}


COLORS_4 = {
    **COLORS_3,
    **{
        (128, 128, 128): 90,  # dark gray
        (255, 0, 0): 91,  # bright red
        (0, 255, 0): 92,  # bright green
        (255, 255, 0): 93,  # bright yellow
        (0, 0, 255): 94,  # bright blue
        (255, 0, 255): 95,  # bright magenta
        (0, 255, 255): 96,  # bright cyan
        (255, 255, 255): 97,  # white
    },
}


def quantize_8_bit(ansi_code: int, to: Literal[3, 4]) -> tuple[int, int, int] | str:
    if 0 <= ansi_code <= 7:
        return f"{30+ansi_code}"

    if 8 <= ansi_code <= 15:
        return f"{(90 if to == 4 else 30) +ansi_code-8}"

    if 232 <= ansi_code <= 255:
        step = int(float(255 / 24) * (255 - ansi_code))
        return (step, step, step)

    n = ansi_code - 16

    g = (n % 36) // 6
    b = n % 6
    r = (n - g - b) // 36

    return (r * 51, g * 51, b * 51)


class _ANSI:
    """Intermiate representation of an ANSI code"""

    def __init__(self, ansi: str) -> None:
        self.old_ansi = ansi
        self.color_3: int | None = None
        self.color_4: int | None = None
        self.color_8: int | None = None
        self.color_24: tuple[int, int, int] | None = None
        self.background: bool = False
        self.bold: bool = False

        ansi_ = ansi.split(";")
        ansi_[0] = ansi_[0].removeprefix("\x1b[")
        ansi_[-1] = ansi_[-1].removesuffix("m")

        if len(ansi_) < 3:
            # only 3 and 4 bit ansi are less than 3 in length
            if ansi_[0] == 1:
                self.bold = True
                color = int(ansi_[1])
            else:
                color = int(ansi_[0])

            if color < 90:
                self.color_3 = color % 10
            else:
                self.color_4 = color % 10

            if 40 <= color <= 47 or 100 <= color <= 107:
                self.background = True

            return

        if ansi_[1] == "5":
            # Handle 8 bit ansi
            self.color_8 = int(ansi_[2])
            self.background = ansi_[0] == 48

        if ansi_[1] == "2":
            # Handle 24 bit ansi
            self.color_24 = (int(ansi_[2]), int(ansi_[3]), int(ansi_[4]))
            self.background = ansi_[0] == 48

    def estimate(
        self, rgb: tuple[int, int, int], colors: dict[tuple[int, int, int], int]
    ) -> str:
        closest = min(colors.keys(), key=lambda x: dist(rgb, x))
        num = colors[closest]
        if self.background:
            num += 10
        return f"\x1b[{num}m"

    def to_3(self) -> str:
        if self.color_24:
            return self.estimate(self.color_24, COLORS_3)

        if self.color_8:
            eight = quantize_8_bit(self.color_8, to=3)

            if isinstance(eight, str):
                return f"\x1b[{eight}m"
            else:
                return self.estimate(eight, COLORS_3)

        if self.color_3:
            color = self.color_3 + 30

        if self.color_4:
            color = self.color_4 + 30

        if self.background:
            color += 10

        if self.bold:
            return f"\x1b[1;{color}m"

        return f"\x1b[{color}m"

    def to_4(self) -> str:
        if self.color_24:
            return self.estimate(self.color_24, COLORS_4)

        if self.color_8:
            eight = quantize_8_bit(self.color_8, to=3)

            if isinstance(eight, str):
                return f"\x1b[{eight}m"
            else:
                return self.estimate(eight, COLORS_4)

        return self.old_ansi

    def to_8(self) -> str:
        if self.color_24:
            r, g, b = self.color_24

            color = 36 * (r // 51) + 6 * (g // 51) + (b // 51)

            return f"\x1b[{48 if self.background else 38};5;{color + 16}m"

        return self.old_ansi


def quantize_ansi(ansi: str, to: Literal[3, 4, 8]) -> str:
    def replace_color(match: Match[str]) -> str:
        m = match.group()
        ansi_ = _ANSI(m)

        if to == 3:
            return ansi_.to_3()
        if to == 4:
            return ansi_.to_4()

        return ansi_.to_8()

    return ANSI_REGEX.sub(replace_color, ansi)
