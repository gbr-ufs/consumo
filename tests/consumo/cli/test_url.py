# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/url module."""

from unittest.mock import MagicMock, patch

from av.error import InvalidDataError
from pydantic import HttpUrl
from pytest import mark
from typer.testing import CliRunner, Result
from yt_dlp.utils import DownloadError

from consumo.cli.url import app
from consumo.lib.exceptions import MissingMetadataError

runner: CliRunner = CliRunner()


@mark.parametrize(
    "url, consumption_time, expected_result",
    [("https://info.cern.ch/hypertext/WWW/TheProject.html", 43, "43s")],
)
@patch("consumo.cli.url.get_hosted_multimedia_duration")
@patch("consumo.cli.url.calculate_consumption_time")
def test_process_urls_downloaderror(
    mock_calculate_consumption_time: MagicMock,
    mock_get_hosted_multimedia_duration: MagicMock,
    url: HttpUrl,
    consumption_time: int,
    expected_result: str,
) -> None:
    mock_get_hosted_multimedia_duration.side_effect = DownloadError("")
    mock_calculate_consumption_time.return_value = consumption_time
    actual_result: Result = runner.invoke(app, [str(url)])
    expected_exit_code: int = 0

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


@mark.parametrize(
    "url, consumption_time, expected_result",
    [
        (
            "https://dn710704.ca.archive.org/0/items/night_of_the_living_dead_dvd/Night.mp4",
            5732,
            "1h 35m 32s",
        )
    ],
)
@patch("consumo.cli.url.get_multimedia_duration")
@patch("consumo.cli.url.get_hosted_multimedia_duration")
def test_process_urls_missingmetadataerror(
    mock_get_hosted_multimedia_duration: MagicMock,
    mock_get_multimedia_duration: MagicMock,
    url: HttpUrl,
    consumption_time: int,
    expected_result: str,
) -> None:
    mock_get_hosted_multimedia_duration.side_effect = MissingMetadataError
    mock_get_multimedia_duration.return_value = consumption_time
    actual_result: Result = runner.invoke(app, [str(url)])
    expected_exit_code: int = 0

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


@mark.parametrize(
    "url, consumption_time, expected_result",
    [
        (
            "https://www.bbc.com/news/articles/c4g0dzg6e4mo",
            297,
            "4m 57s",
        )
    ],
)
@patch("consumo.cli.url.get_hosted_multimedia_duration")
@patch("consumo.cli.url.get_multimedia_duration")
@patch("consumo.cli.url.calculate_consumption_time")
def test_process_urls_invaliddataerror(
    mock_calculate_consumption_time: MagicMock,
    mock_get_multimedia_duration: MagicMock,
    mock_get_hosted_multimedia_duration: MagicMock,
    url: HttpUrl,
    consumption_time: int,
    expected_result: str,
) -> None:
    mock_get_hosted_multimedia_duration.side_effect = MissingMetadataError
    mock_get_multimedia_duration.side_effect: InvalidDataError = InvalidDataError(
        1094995529, "Invalid data found when processing input", str(url)
    )
    mock_calculate_consumption_time.return_value = consumption_time
    actual_result: Result = runner.invoke(app, [str(url)])
    expected_exit_code: int = 0

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


@mark.parametrize(
    "url, consumption_time, expected_result",
    [("https://www.youtube.com/watch?v=H91BxkBXttE", 5717, "1h 35m 17s")],
)
@patch("consumo.cli.url.get_hosted_multimedia_duration")
def test_process_urls_hosted(
    mock_get_hosted_multimedia_duration: MagicMock,
    url: HttpUrl,
    consumption_time: int,
    expected_result: str,
) -> None:
    mock_get_hosted_multimedia_duration.return_value = consumption_time
    actual_result: Result = runner.invoke(app, [str(url)])
    expected_exit_code: int = 0

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


@patch("consumo.cli.core.handle_multiple_args")
def test_process_urls_multiple(mock_handle_multiple_args: MagicMock) -> None:
    mock_handle_multiple_args.return_value: dict[HttpUrl, int] = {
        "https://info.cern.ch/hypertext/WWW/TheProject.html": 43,
        "https://www.bbc.com/news/articles/c4g0dzg6e4mo": 297,
    }
    actual_result: Result = runner.invoke(
        app,
        [
            "https://info.cern.ch/hypertext/WWW/TheProject.html",
            "https://www.bbc.com/news/articles/c4g0dzg6e4mo",
        ],
    )
    expected_exit_code: int = 0

    assert actual_result.exit_code == expected_exit_code

    assert "43s" in actual_result.output
    assert "4m 57s" in actual_result.output
