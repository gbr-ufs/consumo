# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import patch

from av.error import InvalidDataError
from pydantic import HttpUrl
from pytest import mark
from typer.testing import CliRunner, Result
from yt_dlp.utils import DownloadError

from consumo.cli.url import app
from consumo.lib.exceptions import MissingMetadataError
from consumo.lib.types import Second

runner: CliRunner = CliRunner()


@mark.parametrize(
    "url, consumption_time, expected_time",
    [("https://info.cern.ch/hypertext/WWW/TheProject.html", 43, "43s")],
)
@patch("consumo.cli.url.get_video_platform_video_duration")
@patch("consumo.cli.url.calculate_consumption_time")
def test_process_url_downloaderror(
    mock_calculate_consumption_time,
    mock_get_video_platform_video_duration,
    url: HttpUrl,
    consumption_time: Second,
    expected_time: str,
) -> None:
    mock_get_video_platform_video_duration.side_effect = DownloadError("")
    mock_calculate_consumption_time.return_value: Second = consumption_time
    actual_time: Result = runner.invoke(app, [str(url)])
    expected_exit_code: int = 0

    assert actual_time.exit_code == expected_exit_code
    assert expected_time in actual_time.output


@mark.parametrize(
    "url, consumption_time, expected_time",
    [
        (
            "https://dn710704.ca.archive.org/0/items/night_of_the_living_dead_dvd/Night.mp4",
            5732,
            "1h 35m 32s",
        )
    ],
)
@patch("consumo.cli.url.get_multimedia_duration")
@patch("consumo.cli.url.get_video_platform_video_duration")
def test_process_url_missingmetadataerror(
    mock_calculate_consumption_time,
    mock_get_multimedia_duration,
    url: HttpUrl,
    consumption_time: Second,
    expected_time: str,
) -> None:
    mock_get_multimedia_duration.side_effect: MissingMetadataError = (
        MissingMetadataError
    )
    mock_calculate_consumption_time.return_value: Second = consumption_time
    actual_time: Result = runner.invoke(app, [str(url)])
    expected_exit_code: int = 0

    assert actual_time.exit_code == expected_exit_code
    assert expected_time in actual_time.output


@mark.parametrize(
    "url, consumption_time, expected_time",
    [
        (
            "https://www.bbc.com/news/articles/c4g0dzg6e4mo",
            297,
            "4m 57s",
        )
    ],
)
@patch("consumo.cli.url.get_video_platform_video_duration")
@patch("consumo.cli.url.get_multimedia_duration")
@patch("consumo.cli.url.calculate_consumption_time")
def test_process_url_invaliddataerror(
    mock_calculate_consumption_time,
    mock_get_multimedia_duration,
    mock_get_video_platform_video_duration,
    url: HttpUrl,
    consumption_time: Second,
    expected_time: str,
) -> None:
    mock_get_video_platform_video_duration.side_effect: MissingMetadataError = (
        MissingMetadataError
    )
    mock_get_multimedia_duration.side_effect: InvalidDataError = InvalidDataError(
        1094995529, "Invalid data found when processing input", str(url)
    )
    mock_calculate_consumption_time.return_value: Second = consumption_time
    actual_time: Result = runner.invoke(app, [str(url)])
    expected_exit_code: int = 0

    assert actual_time.exit_code == expected_exit_code
    assert expected_time in actual_time.output


@mark.parametrize(
    "url, consumption_time, expected_time",
    [("https://www.youtube.com/watch?v=H91BxkBXttE", 5717, "1h 35m 17s")],
)
@patch("consumo.cli.url.get_video_platform_video_duration")
def test_process_url_video_platform(
    mock_get_video_platform_video_duration,
    url: HttpUrl,
    consumption_time: Second,
    expected_time: str,
) -> None:
    mock_get_video_platform_video_duration.return_value: Second = consumption_time
    actual_time: Result = runner.invoke(app, [str(url)])
    expected_exit_code: int = 0

    assert actual_time.exit_code == expected_exit_code
    assert expected_time in actual_time.output


@patch("consumo.lib.cli.core.handle_multiple_args")
def test_process_url_multiple(mock_handle_multiple_args) -> None:
    mock_handle_multiple_args.return_value: dict[HttpUrl, int] = {
        "https://info.cern.ch/hypertext/WWW/TheProject.html": 43,
        "https://www.bbc.com/news/articles/c4g0dzg6e4mo": 297,
    }
    result: Result = runner.invoke(
        app,
        [
            "https://info.cern.ch/hypertext/WWW/TheProject.html",
            "https://www.bbc.com/news/articles/c4g0dzg6e4mo",
        ],
    )
    expected_exit_code: int = 0

    assert result.exit_code == expected_exit_code

    assert "43s" in result.output
    assert "4m 57s" in result.output
