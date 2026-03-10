# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/file/video module."""

from unittest.mock import MagicMock, patch

import pytest
from pydantic import HttpUrl
from pytest import mark
from yt_dlp.utils import DownloadError

from consumo.lib.exceptions import MissingMetadataError
from consumo.lib.file.video import (
    get_duration,
    get_video_platform_video_duration,
)


@mark.parametrize(
    "url, expected_duration",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", 213),
        ("https://www.youtube.com/watch?v=_-ywSPWu3K8", 5),
    ],
)
@patch("consumo.lib.file.video.YoutubeDL")
def test_get_video_platform_video_duration(
    MockYTDLP: MagicMock, url: str, expected_duration: int
) -> None:
    mock_yt_dlp: MagicMock = MockYTDLP.return_value.__enter__.return_value
    mock_yt_dlp.extract_info.return_value: dict[str, float] = {
        "duration": expected_duration
    }
    actual_duration: int = get_video_platform_video_duration(HttpUrl(url))

    assert actual_duration == expected_duration


@patch("consumo.lib.file.video.YoutubeDL")
def test_get_video_platform_video_duration_unsupported_site(
    MockYTDLP: MagicMock,
) -> None:
    mock_yt_dlp: MagicMock = MockYTDLP.return_value.__enter__.return_value
    mock_yt_dlp.extract_info.return_value: dict[str, None] = {"duration": None}

    with pytest.raises(MissingMetadataError):
        url: HttpUrl = HttpUrl("https://en.wikipedia.org/wiki/Me_at_the_zoo")

        get_video_platform_video_duration(url)


@mark.parametrize(
    "url, expected_duration",
    [("https://www.youtube.com/watch?v=dQw4w9WgXcQ", 213)],
)
@patch("consumo.lib.file.video.get_video_platform_video_duration")
def test_get_duration_video_platform(
    mock_get_video_platform_video_duration: MagicMock,
    url: HttpUrl,
    expected_duration: int,
) -> None:
    mock_get_video_platform_video_duration.return_value = expected_duration
    actual_duration: int = get_duration(url)

    assert actual_duration == expected_duration


@mark.parametrize(
    "url, expected_duration",
    [
        (
            "https://7e802841-ba91-4f78-b9d1-11e3e61b0408.mdnplay.dev/shared-assets/videos/flower.webm",
            6,
        )
    ],
)
@patch("consumo.lib.file.video.get_video_platform_video_duration")
@patch("consumo.lib.file.video.get_multimedia_duration")
def test_get_duration_media_container(
    mock_get_multimedia_duration: MagicMock,
    mock_get_video_platform_video_duration: MagicMock,
    url: HttpUrl,
    expected_duration: int,
) -> None:
    mock_get_video_platform_video_duration.side_effect = MissingMetadataError
    mock_get_multimedia_duration.return_value = expected_duration
    actual_duration: int = get_duration(url)

    assert actual_duration == expected_duration


@mark.parametrize(
    "url",
    ["https://example.com/videos/video.mp4"],
)
@patch("consumo.lib.file.video.get_video_platform_video_duration")
@patch("consumo.lib.file.video.get_multimedia_duration")
def test_get_duration_downloaderror(
    mock_get_media_container_duration: MagicMock,
    mock_get_video_platform_video_duration: MagicMock,
    url: HttpUrl,
) -> None:
    mock_get_video_platform_video_duration.side_effect = DownloadError(
        f"{url} is not a valid URL"
    )
    mock_get_media_container_duration.side_effect = FileNotFoundError(
        2, "No such file or directory", str(url)
    )

    with pytest.raises(FileNotFoundError):
        get_duration(url)
