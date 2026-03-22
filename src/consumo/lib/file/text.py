# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing text files."""

import math

import regex
from pydantic import FilePath, NonNegativeInt, validate_call


def get_word_count(text: str) -> int:
    """Get the number of words from text.

    Supports Chinese, Japanese, and Korean (CJK) by counting a CJK character as
    a approximately half a word (0.53). This is done because, in the Medium
    formula, the average reading speed for words is 265 per minute, while the
    average for non-alphabetical languages is 500 per character.

    Args:
        text: Text where the number of words will be counted from.

    Returns:
        The number of words in the text.
    """
    raw_result: float = len(text.split())
    cjk = regex.compile(r"\p{Script=Han}|\p{Hiragana}|\p{Katakana}|\p{Script=Hangul}")
    cjk_character_count: int = len(cjk.findall(text))

    # The default reading speed for alphabetical languages in the Medium
    # formula is 265 words per minute. In non-alphabetical ones, it's
    # 500 characters per minute.
    # 265 / 500 = 0.53
    raw_result += cjk_character_count * 0.53

    return math.ceil(raw_result)


@validate_call
def calculate_reading_time(
    word_count: int, words_per_minute: NonNegativeInt = 265
) -> int:
    """Calculate the reading time in seconds based on word count.

    Args:
        word_count: The number of words in the text.
        words_per_minute: Reading speed in words per minute.

    Returns:
        How long in seconds it would take to read the text.
    """
    minutes_to_seconds: int = 60
    raw_reading_time: int | float = (word_count / words_per_minute) * minutes_to_seconds
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
    word_count: int = get_word_count(text)

    return calculate_reading_time(word_count, words_per_minute)
