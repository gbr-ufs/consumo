# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/file/text module."""

from pydantic import FilePath
from pytest import mark

from consumo.lib.file.text import (
    calculate_consumption_time,
    calculate_reading_time,
    get_word_count,
)
from tests import FIXTURES_DIR


@mark.parametrize(
    "text, expected_word_count",
    [
        ("a", 1),
        ("", 0),
        (
            "Th3i1s 14214i1244is s4i24i14pposed t0 be 12 w0892415ords.\nUNTITLED\n1. \n1. Title Page",
            12,
        ),
    ],
)
def test_get_word_count(text: str, expected_word_count: int) -> None:
    actual_word_count: int = get_word_count(text)

    assert actual_word_count == expected_word_count


@mark.parametrize("word_count, words_per_minute", [(265, 265), (1000, 1000)])
def test_calculate_reading_time(word_count: int, words_per_minute: int) -> None:
    actual_reading_time: int = calculate_reading_time(word_count, words_per_minute)
    expected_reading_time: int = 60

    assert actual_reading_time == expected_reading_time


def test_calculate_consumption_time() -> None:
    container: FilePath = FIXTURES_DIR / "README.md"
    actual_consumption_time: int = calculate_consumption_time(container)
    expected_consumption_time: int = 99

    assert actual_consumption_time == expected_consumption_time
