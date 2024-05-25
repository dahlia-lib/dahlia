from __future__ import annotations

import re
from typing import TYPE_CHECKING

from dahlia.constants import ANSI_REGEX, CODE_REGEXES, NO_GROUP_CODES

if TYPE_CHECKING:
    from collections.abc import Iterator


def clean(string: str, marker: str = "&") -> str:
    """Removes all Dahlia codes from a string."""
    for code, *_ in _find_codes(string, _with_marker(marker)):
        string = string.replace(code, marker if code[1] == "_" else "")
    return string


def clean_ansi(string: str) -> str:
    """Removes all ANSI codes from a string."""
    for ansi_code in set(_find_ansi_codes(string)):
        string = string.replace(ansi_code, "")
    return string


def _find_codes(
    string: str, patterns: list[re.Pattern[str]]
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
    return {match.group(0) for match in ANSI_REGEX.finditer(string)}


def _with_marker(marker: str) -> list[re.Pattern[str]]:
    if len(marker) != 1:
        msg = "The marker has to be a single character"
        raise ValueError(msg)
    return [re.compile(marker + i) for i in CODE_REGEXES]
