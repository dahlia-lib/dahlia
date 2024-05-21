from __future__ import annotations

from re import Pattern, compile

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


def _find_codes(
    string: str, patterns: list[Pattern[str]]
) -> list[tuple[str, bool, str]]:
    return [
        (match[0], match[1] == "~", match[2])
        if match.group(0)[1] != "_"
        else (x := match.group(0), x, x)
        for pattern in patterns
        for match in pattern.finditer(string)
    ]


def _find_ansi_codes(string: str) -> list[str]:
    return [
        match.group(0) for pattern in ANSI_REGEXES for match in pattern.finditer(string)
    ]


def _with_marker(marker: str) -> list[Pattern[str]]:
    if len(marker) != 1:
        msg = "The marker has to be a single character"
        raise ValueError(msg)
    return [compile(marker + i) for i in CODE_REGEXES]
