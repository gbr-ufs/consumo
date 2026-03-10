# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/url module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import FilePath, HttpUrl, ValidationError

from consumo.lib.url import (
    calculate_consumption_time,
    get_relative_path_video_duration,
    get_video_duration,
)
from tests import FIXTURES_DIR


@patch("consumo.lib.url.get_absolute_path_video_duration")
def test_get_relative_path_video_duration(
    mock_get_absolute_path_video_duration: MagicMock,
) -> None:
    mock_get_absolute_path_video_duration.return_value = 11
    url: HttpUrl = HttpUrl("https://www.w3schools.com/html/html5_video.asp")
    video: FilePath = Path("mov_bbb.mp4")
    actual_duration: int = get_relative_path_video_duration(url, video)
    expected_duration: int = 11

    assert actual_duration == expected_duration


@patch("consumo.lib.url.get_absolute_path_video_duration")
@patch("consumo.lib.url.get_relative_path_video_duration")
def test_get_video_duration(
    mock_get_relative_path_video_duration: MagicMock,
    mock_get_absolute_path_video_duration: MagicMock,
) -> None:
    mock_get_absolute_path_video_duration.side_effect = ValidationError
    mock_get_relative_path_video_duration.return_value = 11
    url: HttpUrl = HttpUrl("https://www.w3schools.com/html/html5_video.asp")
    video: FilePath = Path("mov_bbb.mp4")
    actual_duration: int = get_video_duration(url, str(video))
    expected_duration: int = 11

    assert actual_duration == expected_duration


@patch("consumo.lib.url.fetch_url")
@patch("consumo.lib.url.get_relative_path_video_duration")
@patch("consumo.lib.url.get_absolute_path_video_duration")
def test_calculate_consumption_time(
    mock_get_absolute_path_video_duration: MagicMock,
    mock_get_relative_path_video_duration: MagicMock,
    mock_fetch_url: MagicMock,
) -> None:
    url: HttpUrl = HttpUrl("https://example.com/url")
    html: FilePath = FIXTURES_DIR / "url.html"
    mock_fetch_url.return_value: str = html.read_text("utf-8")
    mock_get_absolute_path_video_duration.return_value: int = 211
    mock_get_relative_path_video_duration.return_value: int = 1
    actual_time: int = calculate_consumption_time(url)
    expected_time: int = 260

    assert actual_time == expected_time


@patch("consumo.lib.url.fetch_url")
def test_calculate_consumption_time_connectionerror(mock_fetch_url: MagicMock) -> None:
    url: HttpUrl = HttpUrl("https://example.com/url")
    mock_fetch_url.return_value: None = None

    with pytest.raises(ConnectionError):
        calculate_consumption_time(url)
