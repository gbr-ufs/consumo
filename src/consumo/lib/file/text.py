# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing text files."""

import math

import regex
from pydantic import FilePath, NonNegativeInt, validate_call


def get_word_count(text: str) -> tuple[int, int]:
    """Get the number of words from text.

    Args:
        text: Text where the number of words will be counted from.

    Returns:
        The number of words in the text.
    """
    word_count: float = len(text.split())
    cjk = regex.compile(r"\p{Script=Han}|\p{Hiragana}|\p{Katakana}|\p{Script=Hangul}")
    cjk_character_count: int = len(cjk.findall(text))

    return word_count, cjk_character_count


@validate_call
def calculate_reading_time(
    word_count: int, cjk_character_count, words_per_minute: NonNegativeInt = 265
) -> int:
    """Calculate the reading time in seconds based on word count.

    Supports Chinese, Japanese, and Korean (CJK) by having its reading speed as
    1.8867924528 (500 / 265) that of the word one. This is done because, in the Medium
    formula, the average reading speed for words is 265 per minute, while the
    average for non-alphabetical languages is 500 per character.

    Args:
        word_count: The number of words in the text.
        cjk_character_count: The number of CJK characters in the text.
        words_per_minute: Reading speed in words per minute.

    Returns:
        How long in seconds it would take to read the text.
    """
    minutes_to_seconds: int = 60
    raw_word_reading_time: int | float = (
        word_count / words_per_minute
    ) * minutes_to_seconds
    # 500 / 265 \approx 1.8867924528301887.
    cjk_reading_rate: int | float = words_per_minute * 1.8867924528301887
    raw_cjk_reading_time: int | float = cjk_character_count
    raw_reading_time: int | float = raw_word_reading_time + raw_cjk_reading_time
    reading_time: int = math.ceil(raw_reading_time)

    return reading_time


def calculate_consumption_time(
    container: FilePath, words_per_minute: NonNegativeInt = 265
) -> int:
    """Calculate the consumption time of a plain text file in seconds.

    Args:
        container: Path to the plain text file whose consumption time will be
            calculated.
        words_per_minute: Reading speed in words per minute.

    Returns:
        The time in seconds to consume the content in the plain text file.
    """
    text: str = container.read_text("utf-8")
    word_count, cjk_character_count = get_word_count(text)

    return calculate_reading_time(word_count, cjk_character_count, words_per_minute)
