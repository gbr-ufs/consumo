# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing HTML files."""

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta
from pathlib import Path
from typing import Callable, Optional

from bs4 import BeautifulSoup, ResultSet, Tag
from bs4.element import AttributeValueList
from pydantic import (
    FilePath,
    HttpUrl,
    PositiveInt,
    TypeAdapter,
    ValidationError,
    validate_call,
)
from trafilatura import extract

from consumo.lib.file.image import calculate_viewing_time
from consumo.lib.file.multimedia import get_duration as get_multimedia_duration
from consumo.lib.file.text import calculate_reading_time, get_word_count
from consumo.lib.file.video import (
    get_duration as get_absolute_path_video_duration,
)
from consumo.lib.types import Second

DURATION_ADAPTER: TypeAdapter[timedelta] = TypeAdapter(timedelta)


@validate_call
def extract_text(html: FilePath) -> str:
    """Extract the main text content of an HTML file.

    This strips boilerplate content such as headers and footers, and unrelated
    content such as sidebars.

    Args:
        html: Path to the HTML file whose main text content will be extracted.

    Returns:
        The main text content of the HTML file, if any.
    """
    raw_html: str = html.read_text("utf-8")
    text: str | None = extract(raw_html)

    if text is None:
        return ""

    return text


@validate_call
def extract_videos(html: FilePath) -> list[str]:
    """Get all the video sources from an HTML file.

    Args:
        html: Path to the HTML file which we'll get the videos from.

    Returns:
        A list of all the video sources.
    """
    raw_html: str = html.read_text("utf-8")
    soup: BeautifulSoup = BeautifulSoup(raw_html, "lxml")
    iframes: ResultSet[Tag] = soup("iframe")
    videos: ResultSet[Tag] = soup("video")
    result: list[str] = []

    for iframe in iframes:
        src: str | AttributeValueList | None = iframe.get("src")

        result.append(str(src))

    for video in videos:
        primary_source: Tag = video("source")[0]
        src: str | AttributeValueList | None = primary_source.get("src")

        result.append(str(src))

    return result


@validate_call
def get_image_count(html: FilePath) -> int:
    """Get the number of images in an HTML file.

    Args:
        html: Path to the HTML file whose number of images will be counted.

    Returns:
        The number of images in the file.
    """
    raw_html: str = html.read_text("utf-8")
    soup: BeautifulSoup = BeautifulSoup(raw_html, "lxml")

    return len(soup("img"))


@validate_call
def get_relative_path_video_duration(html: FilePath, video: Path) -> Second:
    """Get the duration of a video with a relative path.

    Args:
        html: Path to the original HTML file containing the video.
        video: Relative path to the video, to be resolved based on the HTML
            file's path.

    Returns:
        The duration of the video.
    """
    return get_multimedia_duration(html.parent / video)


@validate_call
def get_video_duration(html: FilePath, video: str) -> Second:
    """Get the duration of a video in an HTML file.

    Tries to treat the video as if it was hosted online, then tries to resolve
    its path if that fails.

    Args:
        html: Path to the HTML file where the video was found.
        video: Path used for the video's "src" attribute.

    Returns:
        The duration of the video in seconds.
    """
    try:
        return get_absolute_path_video_duration(HttpUrl(video))
    except ValidationError:
        # If HttpUrl(video) fails validation, the "src" is likely a relative
        # path rather than a URL.
        return get_relative_path_video_duration(html, Path(video))


@validate_call
def get_custom_player_duration(html: FilePath) -> Second:
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
    soup: BeautifulSoup = BeautifulSoup(raw_html, "lxml")
    script_attrs = {"data-schema": "video-object"}

    found_script_tags: ResultSet[Tag] = soup("script", script_attrs)
    total_seconds: int = 0

    for tag in found_script_tags:
        if not tag.string:
            continue

        try:
            data = json.loads(tag.string)
            duration_str: str | None = data.get("duration")

            if duration_str:
                duration = DURATION_ADAPTER.validate_python(duration_str)

                total_seconds += int(duration.total_seconds())

        except Exception:
            continue

    return total_seconds


@validate_call
def calculate_consumption_time(
    html: FilePath,
    words_per_minute: PositiveInt = 265,
    video_duration_resolver: Optional[Callable[[str], Second]] = None,
) -> Second:
    """Calculate the consumption time of an HTML file in seconds.

    Uses concurrency to get the duration of any videos in the file to avoid any
    possible throttling.

    Args:
        html: Path to the HTML file whose consumption time will be calculated.
        words_per_minute: Reading speed in words per minute.
        video_duration_resolver: Function used to get the duration of a video.

    Returns:
        The time in seconds to consume the content of the HTML file.
    """
    # This is the default video duration resolver. It can't be set as the
    # default in the function parameters because it seems like you can't reuse
    # function parameters in Python.
    if video_duration_resolver is None:

        def video_duration_resolver(video: str) -> Second:
            return get_video_duration(html, video)

    text: str = extract_text(html)
    word_count: int = get_word_count(text)
    reading_time: Second = calculate_reading_time(word_count, words_per_minute)

    image_count: int = get_image_count(html)
    image_time: Second = calculate_viewing_time(image_count)

    videos: list[str] = extract_videos(html)
    video_time: Second = 0

    with ThreadPoolExecutor() as e:
        future_to_video = {
            e.submit(video_duration_resolver, video): video for video in videos
        }

        for future in as_completed(future_to_video):
            video_time += future.result()

    video_time += get_custom_player_duration(html)

    return reading_time + image_time + video_time
