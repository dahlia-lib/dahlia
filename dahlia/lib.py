from __future__ import annotations

from enum import Enum
from os import getenv
from typing import Any, Literal, cast

from dahlia.constants import (
    BG_FORMAT_TEMPLATES,
    COLOR_SETS,
    COLORS_24BIT,
    FORMAT_TEMPLATES,
    FORMATTERS,
    RESET,
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

    _depth: Literal[3, 4, 8, 24] | None

    def __init__(
        self,
        *,
        depth: Depth
        | Literal["tty", "low", "medium", "high", 3, 4, 8, 24]
        | None = None,
        marker: str = "&",
        auto_reset: bool = True,
    ) -> None:
        self._no_color = False
        if depth is None:
            depth_ = _resolve_depth()
            self._no_color = depth_ is None
            self._depth = depth_ and depth_.value
        elif isinstance(depth, int):
            self._depth = Depth(depth).value
        elif isinstance(depth, str):
            self._depth = Depth[depth.upper()].value
        else:
            self._depth = depth.value
        self._marker = marker
        self._auto_reset = auto_reset
        self._patterns = _with_marker(marker)
        self._reset = marker + "R"
        self._hash_fields = (self._depth, self._auto_reset, self._marker)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dahlia):
            return NotImplemented
        return self._hash_fields == other._hash_fields

    def __hash__(self) -> int:
        return hash(self._hash_fields)

    def __repr__(self) -> str:
        return (
            f"Dahlia(depth={self._depth}, "
            f"auto_reset={self._auto_reset}, marker={self._marker!r})"
        )

    @property
    def depth(self) -> Depth | None:
        """Specifies what ANSI color set to use (in bits)."""
        return self._depth and Depth(self._depth)

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
        if not string.endswith(self._reset) and self.auto_reset:
            string += self._reset
        for code, bg, color in _find_codes(string, self._patterns):
            string = string.replace(code, self._get_ansi(color, bg=bg))
        return string.replace(self._marker + "_", self._marker)

    def input(self, prompt: str) -> str:
        """Wraps the built-in `input` by transforming the prompt."""
        return input(self.convert(prompt))

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Wraps the built-in `print` by transforming all of its args."""
        print(*map(self.convert, map(str, args)), **kwargs)

    def _get_ansi(self, code: str, *, bg: bool | None) -> str:
        if code == "R":
            return "\033[0m"
        if code == "_":
            return self._marker + code
        if code[0] == "r":
            return f"\033[{RESET[code[1]]}m"
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

        depth = cast(int, self._depth)
        template = formats[depth]
        if depth == 24:
            r, g, b = COLORS_24BIT[code]
            return template.format(r, g, b)

        color_map = COLOR_SETS[depth]
        value = color_map[code]
        if depth <= 4 and bg:
            value += 10
        return template.format(value)


def _resolve_depth() -> Depth | None:
    if getenv("NO_COLOR") or (term := getenv("TERM", "")) == "dumb":
        return None
    if getenv("COLORTERM") in {"truecolor", "24bit"}:
        return Depth.HIGH
    if term in {"terminator", "mosh"} or "24bit" in term or "24-bit" in term:
        return Depth.HIGH
    if "256" in term:
        return Depth.MEDIUM
    return Depth.LOW
