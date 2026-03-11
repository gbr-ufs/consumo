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


@pytest.mark.parametrize(
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


@pytest.mark.parametrize(
    "text, expected_word_count",
    [
        (
            """
起来！ 不愿做奴隶的人们！
把我们的血肉， 筑成我们新的长城！
中华民族到了最危险的时候，
每个人被迫着发出最后的吼声。
起来！ 起来！ 起来！
我们万众一心，
冒着敌人的炮火， 前进！
冒着敌人的炮火， 前进！
前进！ 前进！ 进！
""",
            101,
        ),
        (
            """
君が代は
千代に八千代に
さざれ石の
巌となりて
苔のむすまで
""",
            32,
        ),
        (
            """
동해 물과 백두산이 마르고 닳도록,
하느님이 보우하사 우리나라 만세.
무궁화 삼천리 화려 강산,
대한 사람 대한으로 길이 보전하세.
남산 위에 저 소나무 철갑을 두른 듯
바람서리 불변함은 우리 기상일세.
가을 하늘 공활한데 높고 구름 없이
밝은 달은 우리 가슴 일편단심일세.
이 기상과 이 맘으로 충성을 다하여
괴로우나 즐거우나 나라 사랑하세.
""",
            186,
        ),
    ],
)
def test_get_word_count_cjk(text: str, expected_word_count: int) -> None:
    actual_word_count: int = get_word_count(text)

    assert actual_word_count == expected_word_count


@pytest.mark.parametrize(
    "text, expected_word_count",
    [
        (
            """
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
""",
            181,
        ),
    ],
)
def test_get_word_count_mixed(text: str, expected_word_count: int) -> None:
    actual_word_count: int = get_word_count(text)

    assert actual_word_count == expected_word_count


@pytest.mark.parametrize("word_count, words_per_minute", [(265, 265), (1000, 1000)])
def test_calculate_reading_time(word_count: int, words_per_minute: int) -> None:
    actual_reading_time: int = calculate_reading_time(word_count, words_per_minute)
    expected_reading_time: int = 60

    assert actual_reading_time == expected_reading_time


def test_calculate_consumption_time() -> None:
    container: FilePath = FIXTURES_DIR / "README.md"
    actual_consumption_time: int = calculate_consumption_time(container)
    expected_consumption_time: int = 99

    assert actual_consumption_time == expected_consumption_time
