# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import Mock, patch

from pydantic import FilePath, HttpUrl
from pytest import mark

from consumo.lib.file.html import (
    calculate_consumption_time,
    extract_text,
    extract_videos,
    get_custom_player_duration,
    get_image_count,
    get_relative_path_video_duration,
)
from consumo.lib.types import Second
from tests import FIXTURES_DIR


@mark.parametrize(
    "filename, expected_text",
    [
        (
            "blog_post.html",
            "The Blog\nBlog Post\nThis is a Blog Post.\nWelcome to my blog. This is my first blog post. 🙂",
        ),
        ("iframe.html", ""),
        ("image.html", ""),
        ("video.html", ""),
    ],
)
def test_extract_text(filename: FilePath, expected_text: str) -> None:
    html: FilePath = FIXTURES_DIR / filename
    actual_text: str = extract_text(html)

    assert actual_text == expected_text


@mark.parametrize(
    "filename, expected_videos",
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
def test_extract_videos(filename: FilePath, expected_videos: list[HttpUrl]) -> None:
    html: FilePath = FIXTURES_DIR / filename
    actual_videos: list[str] = extract_videos(html)

    assert actual_videos == expected_videos


@mark.parametrize(
    "filename, expected_image_count",
    [("blog_post.html", 2), ("iframe.html", 0), ("image.html", 1), ("video.html", 0)],
)
def test_get_image_count(filename: FilePath, expected_image_count: int) -> None:
    html: FilePath = FIXTURES_DIR / filename
    actual_image_count: int = get_image_count(html)

    assert actual_image_count == expected_image_count


def test_get_relative_path_video_duration() -> None:
    html: FilePath = FIXTURES_DIR / "video.html"
    video: FilePath = Path("video.mkv")
    actual_duration: Second = get_relative_path_video_duration(html, video)
    expected_duration: Second = 1

    assert actual_duration == expected_duration


@mark.parametrize(
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
def test_get_custom_player_duration(
    filename: FilePath, expected_duration: Second
) -> None:
    html: FilePath = FIXTURES_DIR / filename
    actual_duration: Second = get_custom_player_duration(html)

    assert actual_duration == expected_duration


@mark.parametrize(
    "filename, expected_time",
    [
        ("blog_post.html", 28),
        ("image.html", 12),
        ("video.html", 1),
    ],
)
def test_calculate_consumption_time(filename: FilePath, expected_time: Second) -> None:
    html: FilePath = FIXTURES_DIR / filename
    actual_time: Second = calculate_consumption_time(html)

    assert actual_time == expected_time


@patch("consumo.lib.file.html.get_absolute_path_video_duration")
def test_calculate_consumption_time_online_video(
    get_absolute_path_video_duration: Mock,
) -> None:
    get_absolute_path_video_duration.return_value = 213
    html: FilePath = FIXTURES_DIR / "iframe.html"
    actual_time: Second = calculate_consumption_time(html)
    expected_time: Second = 213

    assert actual_time == expected_time
