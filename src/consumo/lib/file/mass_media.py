# SPDX-License-Identifier: GPL-3.0-or-later

import pymupdf
from pydantic import FilePath, PositiveInt, validate_call

from consumo.lib.file.text import calculate_reading_time, get_word_count
from consumo.lib.types import Second


@validate_call
def extract_text(container: FilePath) -> str:
    with pymupdf.open(container) as c:
        raw_text: str = " ".join(page.get_text() for page in c)

        return raw_text.strip()


@validate_call
def calculate_consumption_time(
    container: FilePath, words_per_minute: PositiveInt = 265
) -> Second:
    text: str = extract_text(container)
    word_count: int = get_word_count(text)
    reading_time: Second = calculate_reading_time(word_count, words_per_minute)

    return reading_time
