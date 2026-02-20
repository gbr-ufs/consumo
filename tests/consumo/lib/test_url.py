# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from pydantic import FilePath, HttpUrl, ValidationError

from consumo.lib.types import Second
from consumo.lib.url import (
    calculate_consumption_time,
    get_relative_path_video_duration,
    get_video_duration,
)
from tests import FIXTURES_DIR


@patch("consumo.lib.url.get_absolute_path_video_duration")
def test_get_relative_path_video_duration(
    get_absolute_path_video_duration: Mock,
) -> None:
    get_absolute_path_video_duration.return_value = 11
    url: HttpUrl = HttpUrl("https://www.w3schools.com/html/html5_video.asp")
    video: FilePath = Path("mov_bbb.mp4")
    actual_duration: Second = get_relative_path_video_duration(url, video)
    expected_duration: Second = 11

    assert actual_duration == expected_duration


@patch("consumo.lib.url.get_absolute_path_video_duration")
@patch("consumo.lib.url.get_relative_path_video_duration")
def test_get_video_duration(
    get_relative_path_video_duration: Mock,
    get_absolute_path_video_duration: Mock,
) -> None:
    get_absolute_path_video_duration.side_effect = ValidationError
    get_relative_path_video_duration.return_value = 11
    url: HttpUrl = HttpUrl("https://www.w3schools.com/html/html5_video.asp")
    video: FilePath = Path("mov_bbb.mp4")
    actual_duration: Second = get_video_duration(url, str(video))
    expected_duration: Second = 11

    assert actual_duration == expected_duration


@patch("consumo.lib.url.fetch_url")
@patch("consumo.lib.url.get_relative_path_video_duration")
@patch("consumo.lib.url.get_absolute_path_video_duration")
def test_calculate_consumption_time(
    get_absolute_path_video_duration: Mock,
    get_relative_path_video_duration: Mock,
    fetch_url: Mock,
) -> None:
    url: HttpUrl = HttpUrl("https://example.com/url")
    html: FilePath = FIXTURES_DIR / "url.html"
    fetch_url.return_value: str = html.read_text("utf-8")
    get_absolute_path_video_duration.return_value: Second = 211
    get_relative_path_video_duration.return_value: Second = 1
    actual_time: Second = calculate_consumption_time(url)
    expected_time: Second = 260

    assert actual_time == expected_time


@patch("consumo.lib.url.fetch_url")
def test_calculate_consumption_time_connectionerror(fetch_url: Mock) -> None:
    url: HttpUrl = HttpUrl("https://example.com/url")
    fetch_url.return_value: None = None

    with pytest.raises(ConnectionError):
        calculate_consumption_time(url)
