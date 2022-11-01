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
