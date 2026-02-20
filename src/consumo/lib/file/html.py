# SPDX-License-Identifier: GPL-3.0-or-later

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
    raw_html: str = html.read_text("utf-8")
    text: str | None = extract(raw_html)

    if text is None:
        return ""

    return text


@validate_call
def extract_videos(html: FilePath) -> list[str]:
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
    raw_html: str = html.read_text("utf-8")
    soup: BeautifulSoup = BeautifulSoup(raw_html, "lxml")

    return len(soup("img"))


@validate_call
def get_relative_path_video_duration(html: FilePath, video: Path) -> Second:
    return get_multimedia_duration(html.parent / video)


@validate_call
def get_video_duration(html: FilePath, video: str) -> Second:
    try:
        return get_absolute_path_video_duration(HttpUrl(video))
    except ValidationError:
        return get_relative_path_video_duration(html, Path(video))


@validate_call
def get_custom_player_duration(html: FilePath) -> Second:
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
