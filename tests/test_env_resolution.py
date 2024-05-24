from __future__ import annotations

from unittest.mock import patch

import pytest

from dahlia.lib import Dahlia, Depth


@pytest.mark.parametrize(
    ("term", "colorterm", "expected"),
    [
        ("terminator", "foobar", Depth.HIGH),
        ("mosh", "foobar", Depth.HIGH),
        ("xterm-24bit", None, Depth.HIGH),
        (None, None, Depth.LOW),
        ("xterm-24-bit", None, Depth.HIGH),
        ("mosh", "truecolor", Depth.HIGH),
        ("vt", "foobar", Depth.LOW),
        (None, "truecolor", Depth.HIGH),
        ("xterm-ghostty", "24bit", Depth.HIGH),
        ("dumb", "foobar", None),
        ("vt", None, Depth.LOW),
        ("xterm-256color", None, Depth.MEDIUM),
        ("xterm-256color", "truecolor", Depth.HIGH),
    ],
)
def test_depth_resolution(
    term: str | None, colorterm: str | None, expected: Depth
) -> None:
    env = {k: v for k, v in (("TERM", term), ("COLORTERM", colorterm)) if v is not None}
    with patch("dahlia.lib.getenv", env.get):
        assert Dahlia().depth is expected


@pytest.mark.parametrize(
    "env",
    [
        {"TERM": "dumb"},
        {"NO_COLOR": "1"},
        {"NO_COLOR": "true"},
        {"NO_COLOR": "0"},
    ],
)
def test_dumb_term_is_no_color(env: dict[str, str]) -> None:
    with patch("os.environ", env):
        assert Dahlia().convert("&3x") == "x"


@pytest.mark.parametrize(
    "env",
    [
        {"NO_COLOR": ""},
        {"TERM": "some-term"},
        {},
    ],
)
def test_no_color_not_handled(env: dict[str, str]) -> None:
    with patch("os.environ", env):
        assert Dahlia(depth=3).convert("&3x") == "\x1b[36mx\x1b[0m"
