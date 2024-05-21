from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from dahlia.constants import (
    BG_FORMAT_TEMPLATES,
    COLOR_SETS,
    COLORS_24BIT,
    FORMAT_TEMPLATES,
    FORMATTERS,
    NO_COLOR,
)
from dahlia.utils import _find_codes, _with_marker, clean


class Depth(Enum):
    """Specifies usable color depth levels."""

    TTY = 3
    """3-bit color (tty)"""
    LOW = 4
    """4-bit color"""
    MEDIUM = 8
    """8-bit color"""
    HIGH = 24
    """24-bit color (true color)"""


class Dahlia:
    """The main Dahlia class handling string transformations."""
    __slots__ = (
        "_auto_reset",
        "_depth",
        "_hash_fields",
        "_marker",
        "_no_color",
        "_patterns",
        "_reset",
    )

    def __init__(
        self,
        *,
        depth: Depth | Literal["tty", "low", "medium", "high", 3, 4, 8, 24] = Depth.LOW,
        marker: str = "&",
        auto_reset: bool = True,
    ) -> None:
        if isinstance(depth, int):
            depth = Depth(depth)
        elif isinstance(depth, str):
            depth = Depth.__members__[depth.upper()]
        self._depth = depth.value
        self._marker = marker
        self._no_color = NO_COLOR if no_color is None else no_color
        self._auto_reset = auto_reset
        self._patterns = _with_marker(marker)
        self._reset = marker + "r"
        self._hash_fields = (self._depth, self._auto_reset, self._marker)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dahlia):
            return NotImplemented
        return self._hash_fields == other._hash_fields

    def __hash__(self) -> int:
        return hash(self._hash_fields)

    def __repr__(self) -> str:
        return (
            f"Dahlia(depth={self.depth}, "
            f"auto_reset={self.auto_reset}, marker={self.marker!r})"
        )

    @property
    def depth(self) -> int:
        """Specifies what ANSI color set to use (in bits)."""
        return self._depth

    @property
    def marker(self) -> str:
        """Specifies the prefix used by format codes ("&" by default)."""
        return self._marker

    @property
    def auto_reset(self) -> bool:
        """When True, appends a full reset code to the transformed string."""
        return self._auto_reset

    def convert(self, string: str) -> str:
        """Transforms a Dahlia string to an ANSI string."""
        if self._no_color:
            return clean(string)
        if not (string.endswith(self._reset) or self.auto_reset):
            string += self._reset
        for code, bg, color in _find_codes(string, self._patterns):
            string = string.replace(code, self.__get_ansi(color, bg=bg))
        return string.replace(self._marker + "_", self._marker)

    def input(self, prompt: str) -> str:
        """Wraps the built-in `input` by transforming the prompt."""
        return input(self.convert(prompt))

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Wraps the built-in `print` by transforming all of its args."""
        print(*map(self.convert, map(str, args)), **kwargs)

    def reset(self) -> None:
        """Resets all modifiers."""
        self.print(self._reset, end="")

    def test(self) -> None:
        """Prints all default format codes and their formatting."""
        self.print(
            "".join(f"{self.marker}{i * 2}" for i in "0123456789abcdef")
            + "&r&ll&r&mm&r&nn&r&oo".replace("&", self.marker)
        )

    def __get_ansi(self, code: str, *, bg: bool) -> str:
        if code == f"{self._marker}_":
            return code
        formats = BG_FORMAT_TEMPLATES if bg else FORMAT_TEMPLATES
        if len(code) in {3, 6}:
            code_size = len(code) // 3
            r, g, b = (
                int(code[i : i + code_size] * (3 - code_size), 16)
                for i in (code_size * i for i in (0, 1, 2))
            )
            return formats[24].format(r, g, b)
        if code in FORMATTERS:
            return formats[3].format(FORMATTERS[code])

        template = formats[self._depth]
        if self.depth == 24:
            r, g, b = COLORS_24BIT[code]
            return template.format(r, g, b)

        color_map = COLOR_SETS[self.depth]
        value = color_map[code]
        if self.depth <= 4 and bg:
            value += 10
        return template.format(value)
