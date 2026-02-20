# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urljoin

from pydantic import HttpUrl, PositiveInt, ValidationError, validate_call
from trafilatura import fetch_url

from consumo.lib.file.html import (
    calculate_consumption_time as calculate_html_consumption_time,
)
from consumo.lib.file.video import get_duration as get_absolute_path_video_duration
from consumo.lib.types import Second


@validate_call
def get_relative_path_video_duration(url: HttpUrl, video: Path) -> Second:
    resolved: str = urljoin(str(url), str(video))

    return get_absolute_path_video_duration(HttpUrl(resolved))


@validate_call
def get_video_duration(url: HttpUrl, video: str) -> Second:
    try:
        return get_absolute_path_video_duration(HttpUrl(video))
    except ValidationError:
        return get_relative_path_video_duration(url, Path(video))


@validate_call
def calculate_consumption_time(
    url: HttpUrl, words_per_minute: PositiveInt = 265
) -> Second:
    html_content: str | None = fetch_url(str(url))

    if html_content is None:
        raise ConnectionError

    with TemporaryDirectory() as tmp_dir:
        html: Path = Path(tmp_dir) / "temp.html"

        html.write_text(html_content, "utf-8")

        return calculate_html_consumption_time(
            html, words_per_minute, lambda video: get_video_duration(url, video)
        )
