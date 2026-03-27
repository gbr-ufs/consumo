# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing mass media files."""

import pymupdf
from pydantic import FilePath, NonNegativeInt, validate_call

from consumo.lib.file.text import calculate_reading_time, get_word_count


@validate_call
def extract_text(container: FilePath) -> str:
    """Extract text from a text container file.

    Args:
        container: Path to a file primarily meant for text. Supported types
            are EPUB, MOBI and PDF.

    Returns:
        All the text content in the container.
    """
    with pymupdf.open(container) as c:
        raw_text: str = " ".join(page.get_text() for page in c)

        return raw_text.strip()


@validate_call
def calculate_consumption_time(
    container: FilePath, words_per_minute: NonNegativeInt = 265
) -> int:
    """Calculate the consumption time of a text container file in seconds.

    Args:
        container: Path to a file primarily meant for text. Supported types
            are EPUB, MOBI and PDF.
        words_per_minute: Reading speed in words per minute.

    Returns:
        The time in seconds to consume the content of the file.
    """
    text: str = extract_text(container)
    word_count, cjk_character_count = get_word_count(text)
    reading_time: int = calculate_reading_time(
        word_count, cjk_character_count, words_per_minute
    )

    return reading_time
