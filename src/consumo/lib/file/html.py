# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing HTML files."""

import json
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from pathlib import Path
from typing import Any, Iterator

import trafilatura
from bs4 import BeautifulSoup, ResultSet, Tag
from bs4.element import AttributeValueList
from pydantic import (
    FilePath,
    HttpUrl,
    NonNegativeInt,
    TypeAdapter,
    ValidationError,
    validate_call,
)

from consumo import beautiful_soup_parser
from consumo.lib.file.image import calculate_viewing_time
from consumo.lib.file.multimedia import (
    get_duration as get_absolute_path_multimedia_duration,
)
from consumo.lib.file.multimedia import (
    get_multimedia_duration as get_not_hosted_multimedia_duration,
)
from consumo.lib.file.text import calculate_reading_time, get_word_count

DURATION_ADAPTER: TypeAdapter[timedelta] = TypeAdapter(timedelta)


def extract_multimedias(soup: BeautifulSoup) -> list[str]:
    """Get all the multimedia sources from an HTML file.

    Args:
        soup: The HTML file as parsed by BeautifulSoup.

    Returns:
        A list of all the multimedia sources.
    """
    audios: ResultSet[Tag] = soup("audio")
    iframes: ResultSet[Tag] = soup("iframe")
    videos: ResultSet[Tag] = soup("video")
    result: list[str] = []

    for audio in audios:
        primary_source: Tag = audio("source")[0]
        src: str | AttributeValueList | None = primary_source.get("src")

        result.append(str(src))

    for iframe in iframes:
        src: str | AttributeValueList | None = iframe.get("src")

        result.append(str(src))

    for video in videos:
        primary_source: Tag = video("source")[0]
        src: str | AttributeValueList | None = primary_source.get("src")

        result.append(str(src))

    return result


@validate_call
def get_relative_path_multimedia_duration(html: FilePath, container: Path) -> int:
    """Get the duration of a multimedia file with a relative path.

    Args:
        html: Path to the original HTML file containing the multimedia file.
        container: Relative path to the multimedia file, to be resolved based
            on the HTML file's path.

    Returns:
        The duration of the content.
    """
    return get_not_hosted_multimedia_duration(html.parent / container)


@validate_call
def get_multimedia_duration(html: FilePath, src: str) -> int:
    """Get the duration of a multimedia file in an HTML file.

    Tries to treat the multimedia file as if it was hosted online, then tries to
    resolve its path if that fails.

    Args:
        html: Path to the HTML file where the multimedia file was found.
        src: Path used for the file's "src" attribute.

    Returns:
        The duration of the content in seconds.
    """
    try:
        return get_absolute_path_multimedia_duration(HttpUrl(src))
    except ValidationError:
        # If HttpUrl(src) fails validation, the src is likely a relative
        # path rather than a URL.
        return get_relative_path_multimedia_duration(html, Path(src))


@validate_call
def get_custom_player_duration(html: FilePath) -> int:
    """Parse the JSON data in an HTML file provided for SEO to get video duration.

    Designed with videos using custom players like the BBC's smp-toucan-player
    in mind.

    The supported format for duration is ISO 8601.

    Args:
        html: Path to the HTML file whose content will be parsed for JSON data
            containing duration information.

    Returns:
        The duration reported by the JSON data as an integer representing
        seconds.
    """
    raw_html: str = html.read_text("utf-8")
    soup: BeautifulSoup = BeautifulSoup(raw_html, beautiful_soup_parser)
    script_attrs = {"data-schema": "video-object"}

    found_script_tags: ResultSet[Tag] = soup("script", script_attrs)
    total_seconds: int = 0

    for tag in found_script_tags:
        if not tag.string:
            continue

        try:
            data: Any = json.loads(tag.string)
            duration_str: str | None = data.get("duration")

            if duration_str:
                duration: timedelta = DURATION_ADAPTER.validate_python(duration_str)

                total_seconds += int(duration.total_seconds())

        except Exception:
            continue

    return total_seconds


@validate_call
def calculate_consumption_time(
    html: FilePath,
    words_per_minute: NonNegativeInt = 265,
    multimedia_duration_resolver=None,  # noqa: ANN001 (unsuppored by Typer)
) -> int:
    """Calculate the consumption time of an HTML file in seconds.

    Uses concurrency to get the duration of any multimedia in the file to avoid any
    possible throttling.

    Args:
        html: Path to the HTML file whose consumption time will be calculated.
        words_per_minute: Reading speed in words per minute.
        multimedia_duration_resolver: Function used to get the duration of a
            multimedia file.

    Returns:
        The time in seconds to consume the content of the HTML file.
    """
    # This is the default multimedia duration resolver. It can't be set as the
    # default in the function parameters because it seems like you can't reuse
    # function parameters in Python.
    if multimedia_duration_resolver is None:

        def multimedia_duration_resolver(src: str) -> int:
            return get_multimedia_duration(html, src)

    raw_html: str = html.read_text("utf-8")
    soup: BeautifulSoup = BeautifulSoup(raw_html, beautiful_soup_parser)
    text: str | None = trafilatura.extract(raw_html)
    word_count, cjk_character_count = get_word_count(text or "")
    reading_time: int = calculate_reading_time(
        word_count, cjk_character_count, words_per_minute
    )

    image_count: int = len(soup("img"))
    image_time: int = calculate_viewing_time(image_count)

    multimedias: list[str] = extract_multimedias(soup)
    multimedia_time: int = 0

    with ThreadPoolExecutor() as e:
        resolved_durations: Iterator[int] = e.map(
            multimedia_duration_resolver, multimedias
        )

        multimedia_time += sum(resolved_durations)

    multimedia_time += get_custom_player_duration(html)

    return reading_time + image_time + multimedia_time
