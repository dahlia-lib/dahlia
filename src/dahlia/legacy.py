from __future__ import annotations

from typing import Any

from .dahlia import Dahlia, Depth


def dprint(
    *args: Any,
    depth: Depth = Depth.LOW,
    no_color: bool | None = None,
    no_reset: bool = False,
    marker: str = "&",
    **kwargs: Any,
) -> None:
    """
    Functional, legacy alternative to ``Dahlia.print``.

    Parameters
    ----------
    *args : Any
        Objects to print
    depth : Depth
        Specifies what ANSI color set to use (in bits)
    no_reset : bool
        When True, doesn't add an "&r" at the end when converting strings
    marker : str
        Specifies the prefix used by format codes ("&" by default)
    """
    Dahlia(depth=depth, no_color=no_color, no_reset=no_reset, marker=marker).print(
        *args, **kwargs
    )


def dahlia(
    string: str,
    *,
    depth: Depth = Depth.LOW,
    no_color: bool | None = None,
    no_reset: bool = False,
    marker: str = "&",
) -> str:
    """
    Functional, legacy alternative to ``Dahlia.convert``.

    Parameters
    ----------
    string : str
        String to format
    depth : Depth
        Specifies what ANSI color set to use (in bits)
    no_reset : bool
        When True, doesn't add an "&r" at the end when converting strings
    marker : str
        Specifies the prefix used by format codes ("&" by default)

    Returns
    -------
    str
        A formatted string with the appropriate formatting applied
    """
    return Dahlia(
        depth=depth, no_color=no_color, no_reset=no_reset, marker=marker
    ).convert(string)
