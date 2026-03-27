# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/file/text module."""

import pytest
from pydantic import FilePath

from consumo.lib.file.text import (
    calculate_consumption_time,
    calculate_reading_time,
    get_word_count,
)
from tests import FIXTURES_DIR


def test_get_word_count_mixed() -> None:
    text: str = """
起来！ 不愿做奴隶的人们！
把我们的血肉， 筑成我们新的长城！
中华民族到了最危险的时候，
每个人被迫着发出最后的吼声。
起来！ 起来！ 起来！
我们万众一心，
冒着敌人的炮火， 前进！
冒着敌人的炮火， 前进！
前进！ 前进！ 进！

O say, can you see, by the dawn's early light,
⁠What so proudly we hailed at the twilight's last gleaming?
Whose broad stripes and bright stars through the perilous fight,
⁠O'er the ramparts we watched, were so gallantly streaming?
And the rockets' red glare, the bombs bursting in air,
Gave proof through the night that our flag was still there;
O say does that star-spangled banner yet wave,
⁠O'er the land of the free and the home of the brave?
"""
    actual_word_count, actual_cjk_character_count = get_word_count(text)
    expected_word_count: int = 97
    expected_cjk_character_count: int = 84

    assert actual_word_count == expected_word_count
    assert actual_cjk_character_count == expected_cjk_character_count


@pytest.mark.parametrize(
    "word_count, cjk_character_count, words_per_minute",
    [(265, 0, 265), (0, 60, 1000)],
)
def test_calculate_reading_time(
    word_count: int, cjk_character_count: int, words_per_minute: int
) -> None:
    actual_reading_time: int = calculate_reading_time(
        word_count, cjk_character_count, words_per_minute
    )
    expected_reading_time: int = 60

    assert actual_reading_time == expected_reading_time


def test_calculate_consumption_time() -> None:
    container: FilePath = FIXTURES_DIR / "README.md"
    actual_consumption_time: int = calculate_consumption_time(container)
    expected_consumption_time: int = 99

    assert actual_consumption_time == expected_consumption_time
