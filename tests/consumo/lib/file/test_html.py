# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/file/html module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from bs4 import BeautifulSoup
from pydantic import FilePath

from consumo.lib.file.html import (
    calculate_consumption_time,
    extract_multimedias,
    get_custom_player_duration,
    get_relative_path_multimedia_duration,
)
from tests import FIXTURES_DIR


@pytest.mark.parametrize(
    "filename, expected_multimedias",
    [
        ("blog_post.html", []),
        ("iframe.html", ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]),
        (
            "image.html",
            [],
        ),
        ("video.html", ["video.mkv"]),
    ],
)
def test_extract_multimedias(filename: str, expected_multimedias: list[str]) -> None:
    html: FilePath = FIXTURES_DIR / filename
    raw_html: str = html.read_text("utf-8")
    soup: BeautifulSoup = BeautifulSoup(raw_html, "lxml")
    actual_multimedias: list[str] = extract_multimedias(soup)

    assert actual_multimedias == expected_multimedias


def test_get_relative_path_multimedia_duration() -> None:
    html: FilePath = FIXTURES_DIR / "video.html"
    src: FilePath = Path("video.mkv")
    actual_duration: int = get_relative_path_multimedia_duration(html, src)
    expected_duration: int = 1

    assert actual_duration == expected_duration


@pytest.mark.parametrize(
    "filename, expected_duration",
    [
        (
            "get_custom_player_duration.html",
            66,
        ),
        (
            "get_custom_player_duration_no_duration.html",
            0,
        ),
        (
            "get_custom_player_duration_empty_script_tag.html",
            0,
        ),
        (
            "get_custom_player_duration_malformed_json.html",
            0,
        ),
        (
            "blog_post.html",
            0,
        ),
    ],
)
def test_get_custom_player_duration(filename: FilePath, expected_duration: int) -> None:
    html: FilePath = FIXTURES_DIR / filename
    actual_duration: int = get_custom_player_duration(html)

    assert actual_duration == expected_duration


@pytest.mark.parametrize(
    "filename, expected_time",
    [
        ("audio.html", 1),
        ("blog_post.html", 28),
        ("image.html", 12),
        ("video.html", 1),
    ],
)
def test_calculate_consumption_time(filename: FilePath, expected_time: int) -> None:
    html: FilePath = FIXTURES_DIR / filename
    actual_time: int = calculate_consumption_time(html)

    assert actual_time == expected_time


@patch("consumo.lib.file.html.get_absolute_path_multimedia_duration")
def test_calculate_consumption_time_online_multimedia(
    mock_get_absolute_path_multimedia_duration: MagicMock,
) -> None:
    mock_get_absolute_path_multimedia_duration.return_value = 213
    html: FilePath = FIXTURES_DIR / "iframe.html"
    actual_time: int = calculate_consumption_time(html)
    expected_time: int = 213

    assert actual_time == expected_time
