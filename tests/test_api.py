from unittest.mock import patch

import pytest

from dahlia.constants import REGEX_BREAKING_MARKERS
from dahlia.lib import Dahlia, Depth


@pytest.mark.parametrize(
    ("depth", "string", "expected"),
    [
        (Depth.HIGH, "foo", "foo"),
        (
            Depth.LOW,
            "&e&nunderlined&rn yellow",
            "\x1b[93m\x1b[4munderlined\x1b[24m yellow",
        ),
        (Depth.MEDIUM, "&7ball", "\x1b[38;5;248mball"),
        (Depth.HIGH, "&7ball", "\x1b[38;2;170;170;170mball"),
        (Depth.TTY, "&kcarcinogen", "\x1b[5mcarcinogen"),
        (Depth.LOW, "&lhyperextension", "\x1b[1mhyperextension"),
        (Depth.MEDIUM, "&hgammopathy", "\x1b[8mgammopathy"),
        (Depth.LOW, "&asupremacism", "\x1b[92msupremacism"),
        (Depth.HIGH, "&mlymphocyte", "\x1b[9mlymphocyte"),
        (Depth.TTY, "&alingualumina", "\x1b[32mlingualumina"),
        (Depth.TTY, "&3filariidae", "\x1b[36mfilariidae"),
        (Depth.LOW, "&4aura", "\x1b[31maura"),
        (Depth.LOW, "&~4aura", "\x1b[41maura"),
        (Depth.TTY, "&r&R", "&r\x1b[0m"),
        (Depth.HIGH, "&9aspergillaceae", "\x1b[38;2;85;85;255maspergillaceae"),
        (Depth.LOW, "&~edemigod", "\x1b[103mdemigod"),
        (Depth.TTY, "&9miller", "\x1b[34mmiller"),
        (Depth.HIGH, "&#ffaff3;gleaming", "\x1b[38;2;255;175;243mgleaming"),
        (Depth.HIGH, "&#fbf;gweaming", "\x1b[38;2;255;187;255mgweaming"),
    ],
)
def test_conversion(depth: Depth, string: str, expected: str) -> None:
    assert Dahlia(depth=depth, auto_reset=False).convert(string) == expected


@pytest.mark.parametrize(
    ("marker", "expected"),
    [
        ("&", "\x1b[93me§ee§§_4x"),
        ("e", "&\x1b[93m§\x1b[93m§§_4x"),
        ("§", "&ee\x1b[93me§§4x"),
        ("_", "&ee§ee§§\x1b[31mx"),
        ("4", "&ee§ee§§_4x"),
        ("x", "&ee§ee§§_4x"),
    ],
)
def test_marker_clashing(marker: str, expected: str) -> None:
    assert (
        Dahlia(marker=marker, auto_reset=False, depth=Depth.LOW).convert("&ee§ee§§_4x")
        == expected
    )


@pytest.mark.parametrize("marker", REGEX_BREAKING_MARKERS)
def test_regex_markers(marker: str) -> None:
    assert (
        Dahlia(depth=Depth.LOW, marker=marker).convert(f"{marker}4xe5")
        == "\x1b[31mxe5\x1b[0m"
    )


@pytest.mark.parametrize("marker", ["", "&&"])
def test_invalid_marker(marker: str) -> None:
    with pytest.raises(ValueError, match="The marker has to be a single character"):
        Dahlia(marker=marker)


@pytest.mark.parametrize("marker", [123, [1], {"key": "value"}])
def test_nonstring_marker(marker: str) -> None:
    with pytest.raises(TypeError, match="The marker has to be a string"):
        Dahlia(marker=marker)


@pytest.mark.parametrize(("auto_reset", "expected"), [(True, "\x1b[0m"), (False, "")])
def test_auto_reset(auto_reset: bool, expected: str) -> None:
    assert Dahlia(auto_reset=auto_reset).convert("") == expected


def test_print(capsys: pytest.CaptureFixture[str]) -> None:
    d = Dahlia()
    content = "&e&nunderlined&rn yellow"
    d.print(content)

    assert capsys.readouterr().out == d.convert(content) + "\n"


def test_print_custom_sep_end(capsys: pytest.CaptureFixture[str]) -> None:
    content = ("&#ffaff3;gleaming", "&bdiamond", "&lcool")
    d = Dahlia()
    d.print(*content, sep=":::", end="!!!")

    assert capsys.readouterr().out == ":::".join(d.convert(c) for c in content) + "!!!"


def test_input(capsys: pytest.CaptureFixture[str]) -> None:
    d = Dahlia(depth=Depth.LOW)
    prompt = "&a&lprompt: "
    with patch(
        "builtins.input", side_effect=lambda _: (print(d.convert(prompt)), "ok")[1]
    ):
        ans = d.input(prompt)

    assert capsys.readouterr().out == d.convert(prompt) + "\n"
    assert ans == "ok"


def test_depth_accepts_case_insensitive_str() -> None:
    assert Dahlia(depth="lOw").depth is Depth.LOW


def test_properties() -> None:
    d = Dahlia(depth=Depth.TTY)
    assert d.marker == "&"
    assert hash(d) == hash(Dahlia(depth=Depth.TTY))
    assert eval(repr(d)) == d  # noqa: S307
    assert d != 1
