from __future__ import annotations

import re
from typing import TYPE_CHECKING

from dahlia.constants import (
    ANSI_REGEX,
    CODE_REGEXES,
    NO_GROUP_CODES,
    REGEX_BREAKING_MARKERS,
)

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator


def clean(string: str, marker: str = "&") -> str:
    """Removes all Dahlia codes from a string."""
    for code, *_ in _find_codes(string, _with_marker(marker)):
        string = string.replace(code, marker if code[1] == "_" else "")
    return string


def clean_ansi(string: str) -> str:
    """Removes all ANSI codes from a string."""
    for ansi_code in _find_ansi_codes(string):
        string = string.replace(ansi_code, "")
    return string


def escape(string: str, marker: str = "&") -> str:
    """Escapes all instances of the marker in a string."""
    return string.replace(marker, marker + "_")


def _find_codes(
    string: str, patterns: Iterable[re.Pattern[str]]
) -> Iterator[tuple[str, bool | None, str]]:
    return reversed(
        dict.fromkeys(
            (match[0], None, match[1])  # full-reset, escape
            if (full_snd_char := match[0][1]) in NO_GROUP_CODES
            else (
                (match[0], None, match[1])  # reset
                if full_snd_char == "r"
                else (match[0], match[1] == "~", match[2])  # regular
            )
            for pattern in patterns
            for match in pattern.finditer(string)
        )
    )


def _find_ansi_codes(string: str) -> set[str]:
    return {match[0] for match in ANSI_REGEX.finditer(string)}


def _with_marker(marker: str) -> list[re.Pattern[str]]:
    if not isinstance(marker, str):
        msg = "The marker has to be a string"
        raise TypeError(msg)
    if len(marker) != 1:
        msg = "The marker has to be a single character"
        raise ValueError(msg)
    if marker in REGEX_BREAKING_MARKERS:
        marker = "\\" + marker
    return [re.compile(marker + i) for i in CODE_REGEXES]
