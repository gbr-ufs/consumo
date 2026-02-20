# SPDX-License-Identifier: GPL-3.0-or-later

import math

from pydantic import FilePath, PositiveInt, validate_call

from consumo.lib.types import DecimalSecond, Second


def get_word_count(text: str) -> int:
    return len(text.split())


@validate_call
def calculate_reading_time(
    word_count: int, words_per_minute: PositiveInt = 265
) -> Second:
    minutes_to_seconds: Second = 60
    raw_reading_time: DecimalSecond = (
        word_count / words_per_minute
    ) * minutes_to_seconds
    reading_time: Second = math.ceil(raw_reading_time)

    return reading_time


def calculate_consumption_time(
    container: FilePath, words_per_minute: PositiveInt = 265
) -> Second:
    text: str = container.read_text("utf-8")
    word_count: int = get_word_count(text)

    return calculate_reading_time(word_count, words_per_minute)
