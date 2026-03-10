# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/file/mass_media module."""

from pydantic import FilePath
from pytest import mark

from consumo.lib.file.mass_media import calculate_consumption_time, extract_text
from tests import FIXTURES_DIR


@mark.parametrize(
    "filename, expected_text",
    [
        ("single_char.pdf", "a"),
        ("empty.epub", ""),
        (
            "jumbled.mobi",
            "Th3i1s 14214i1244is s4i24i14pposed t0 be 12 w0892415ords.\nUNTITLED\n1. \n1. Title Page",
        ),
    ],
)
def test_extract_text(filename: str, expected_text: str) -> None:
    container: FilePath = FIXTURES_DIR / filename
    actual_text: str = extract_text(container)

    assert actual_text == expected_text


@mark.parametrize(
    "filename, words_per_minute, expected_time",
    [("single_char.pdf", 265, 1), ("empty.epub", 265, 0), ("jumbled.mobi", 1000, 1)],
)
def test_calculate_consumption_time(
    filename: str, words_per_minute: int, expected_time: int
) -> None:
    container: FilePath = FIXTURES_DIR / filename
    actual_time: int = calculate_consumption_time(container, words_per_minute)

    assert actual_time == expected_time
