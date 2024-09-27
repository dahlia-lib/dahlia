import pytest

from dahlia.__main__ import TEST_STRING
from dahlia.utils import clean, clean_ansi, escape


@pytest.mark.parametrize(
    ("content", "marker", "expected"),
    [
        ("&e&nunderlined&rn yellow", "&", "underlined yellow"),
        ("&e&nunderlined&rn yellow", "!", "&e&nunderlined&rn yellow"),
        ("!e!nunderlined!rn yellow", "!", "underlined yellow"),
        ("§_4 gives §4red", "§", "§4 gives red"),
    ],
)
def test_clean(content: str, marker: str, expected: str) -> None:
    assert clean(content, marker) == expected


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("\x1b[93m\x1b[4munderlined\x1b[0m yellow", "underlined yellow"),
        ("\x1b[38;2;255;255;85m\x1b[4munderlined\x1b[0m yellow", "underlined yellow"),
        ("\x1bxxx", "\x1bxxx"),
        ("\x1b[xm", "\x1b[xm"),
    ],
)
def test_clean_ansi(content: str, expected: str) -> None:
    assert clean_ansi(content) == expected


def test_cli_test_string() -> None:
    assert clean(TEST_STRING) == "0123456789abcdefhijklmno"


@pytest.mark.parametrize(
    ("content", "marker", "expected"),
    [
        ("&e&nunderlined&rn yellow", "&", "&_e&_nunderlined&_rn yellow"),
        ("&ame & &dher", "&", "&_ame &_ &_dher"),
        ("&e&nunderlined&rn yellow", "!", "&e&nunderlined&rn yellow"),
        ("!e!nunderlined!rn yellow", "!", "!_e!_nunderlined!_rn yellow"),
        ("§_4 gives §4red", "§", "§__4 gives §_4red"),
    ],
)
def test_escape(content: str, marker: str, expected: str) -> None:
    assert escape(content, marker) == expected
