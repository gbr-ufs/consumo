# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing text files."""

import math

from pydantic import FilePath, PositiveInt, validate_call

from consumo.lib.types import DecimalSecond, Second


def get_word_count(text: str) -> int:
    """Get the number of words from text.

    Args:
        text: Text where the number of words will be counted from.

    Returns:
        The number of words in the text.
    """
    return len(text.split())


@validate_call
def calculate_reading_time(
    word_count: int, words_per_minute: PositiveInt = 265
) -> Second:
    """Calculate the reading time in seconds based on word count.

    Args:
        word_count: The number of words in the text.
        words_per_minute: Reading speed in words per minute.

    Returns:
        How long in seconds it would take to read the text.
    """
    minutes_to_seconds: Second = 60
    raw_reading_time: DecimalSecond = (
        word_count / words_per_minute
    ) * minutes_to_seconds
    reading_time: Second = math.ceil(raw_reading_time)

    return reading_time


def calculate_consumption_time(
    container: FilePath, words_per_minute: PositiveInt = 265
) -> Second:
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
