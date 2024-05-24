import pytest

from dahlia.utils import clean, clean_ansi


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
