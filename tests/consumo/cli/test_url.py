# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/url module."""

from sqlite3 import OperationalError
from unittest.mock import MagicMock, Mock, patch

import pytest
from av.error import FFmpegError, InvalidDataError
from pydantic import HttpUrl
from typer.testing import CliRunner, Result
from yt_dlp.utils import DownloadError

from consumo.cli.url import app, get_duration
from consumo.lib.exceptions import MissingMetadataError

runner: CliRunner = CliRunner()


@pytest.mark.parametrize(
    "url, consumption_time, expected_result",
    [("https://info.cern.ch/hypertext/WWW/TheProject.html", 43, "43s")],
)
@patch("consumo.cli.url.get_multimedia_duration")
@patch("consumo.cli.url.calculate_consumption_time")
def test_process_urls_downloaderror(
    mock_calculate_consumption_time: Mock,
    mock_get_multimedia_duration: Mock,
    url: HttpUrl,
    consumption_time: int,
    expected_result: str,
) -> None:
    mock_get_multimedia_duration.side_effect: InvalidDataError = InvalidDataError(
        1094995529, "Invalid data found when processing input", str(url)
    )
    mock_calculate_consumption_time.return_value = consumption_time
    actual_result: Result = runner.invoke(app, [str(url)])
    expected_exit_code: int = 0

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


@pytest.mark.parametrize(
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
def test_process_urls_missingmetadataerror(
    mock_get_multimedia_duration: Mock,
    url: HttpUrl,
    consumption_time: int,
    expected_result: str,
) -> None:
    mock_get_multimedia_duration.return_value = consumption_time
    actual_result: Result = runner.invoke(app, [str(url), "--no-cache"])
    expected_exit_code: int = 0

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


@pytest.mark.parametrize(
    "url, consumption_time, expected_result",
    [
        (
            "https://www.bbc.com/news/articles/c4g0dzg6e4mo",
            297,
            "4m 57s",
        )
    ],
)
@patch("consumo.cli.url.get_multimedia_duration")
@patch("consumo.cli.url.calculate_consumption_time")
def test_process_urls_invaliddataerror(
    mock_calculate_consumption_time: Mock,
    mock_get_multimedia_duration: Mock,
    url: HttpUrl,
    consumption_time: int,
    expected_result: str,
) -> None:
    mock_get_multimedia_duration.side_effect: InvalidDataError = InvalidDataError(
        1094995529, "Invalid data found when processing input", str(url)
    )
    mock_calculate_consumption_time.return_value = consumption_time
    actual_result: Result = runner.invoke(app, [str(url)])
    expected_exit_code: int = 0

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


class FakeDate:
    @staticmethod
    def today():
        # Fixed date for assertions.
        from datetime import date

        return date(2026, 3, 27)


@pytest.mark.parametrize(
    "url, consumption_time, expected_result",
    [("https://www.youtube.com/watch?v=H91BxkBXttE", 5717, "1h 35m 17s")],
)
@patch("consumo.cli.url.cache_result")
@patch("consumo.cli.url.get_hosted_multimedia_duration")
@patch("consumo.cli.url.is_hosted")
@patch("consumo.cli.url.get_cached_result")
@patch("consumo.cli.url.date", new=FakeDate)
def test_process_urls_hosted(
    mock_get_cached_result: Mock,
    mock_is_hosted: Mock,
    mock_get_hosted_multimedia_duration: Mock,
    mock_cache_result: Mock,
    url: HttpUrl,
    consumption_time: int,
    expected_result: str,
) -> None:
    mock_get_cached_result.side_effect = OperationalError
    mock_is_hosted.return_value = True
    mock_get_hosted_multimedia_duration.return_value = consumption_time
    actual_result: Result = runner.invoke(app, [str(url)])
    expected_exit_code: int = 0

    assert mock_cache_result.called
    args: list[str] = mock_cache_result.call_args[0]
    assert args[0] == "consumo"
    assert args[1] == f"{url}:265:0"
    assert args[2] == "2026-03-27"
    assert args[3] == consumption_time
    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


@patch("consumo.cli.core.handle_multiple_args")
def test_process_urls_multiple(mock_handle_multiple_args: Mock) -> None:
    mock_handle_multiple_args.return_value = (
        {
            "https://info.cern.ch/hypertext/WWW/TheProject.html": 43,
            "https://www.bbc.com/news/articles/c4g0dzg6e4mo": 297,
        },
        {},
    )
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


@patch("consumo.cli.url.get_cached_result")
def test_get_duration_cache_hit(
    mock_get_cached_result: Mock,
):
    mock_get_cached_result.return_value = 43

    actual_result: int = get_duration(
        HttpUrl("https://info.cern.ch/hypertext/WWW/TheProject.html")
    )
    expected_result: int = 43

    assert actual_result == expected_result


@patch("consumo.cli.url.cache_result")
@patch("consumo.cli.url.calculate_consumption_time")
@patch("consumo.cli.url.get_multimedia_duration")
@patch("consumo.cli.url.get_cached_result")
@patch("consumo.cli.url.date", new=FakeDate)
def test_get_duration_hosted_success_and_cached(
    mock_get_cached_result: Mock,
    mock_get_multimedia_duration: Mock,
    mock_calculate_consumption_time: Mock,
    mock_cache_result: Mock,
):
    # No cache, hosted resolver succeeds.
    mock_get_cached_result.side_effect = OperationalError
    mock_get_multimedia_duration.side_effect = FFmpegError(1, "", "")
    mock_calculate_consumption_time.return_value = 43

    actual_result: int = get_duration(
        HttpUrl("https://info.cern.ch/hypertext/WWW/TheProject.html")
    )
    expected_result: int = 43

    assert actual_result == expected_result

    # Inspect cache_result call args.
    assert mock_cache_result.called
    args: list[str] = mock_cache_result.call_args[0]
    assert args[0] == "consumo"
    assert args[1] == "https://info.cern.ch/hypertext/WWW/TheProject.html:265:0"
    assert args[2] == "2026-03-27"
    assert args[3] == 43


def test_process_urls_not_a_url_skip_errors() -> None:
    actual_result: Result = runner.invoke(app, [str("file.txt"), "--skip-errors"])
    expected_exit_code: int = 0
    expected_error: str = "ValidationError"

    assert actual_result.exit_code == expected_exit_code
    assert expected_error in actual_result.output


@patch("consumo.cli.url.get_multimedia_duration")
@patch("consumo.cli.url.urllib.request.urlopen")
@patch("consumo.cli.url.calculate_consumption_time")
def test_process_urls_depth(
    mock_calculate_consumption_time: Mock,
    mock_urllib_request_urlopen: Mock,
    mock_get_multimedia_duration: Mock,
) -> None:
    original_url: str = "https://info.cern.ch/"

    mock_get_multimedia_duration.side_effect = FFmpegError(1, "", "")

    def calc_side_effect(url, *args, **kwargs):
        url_result = {
            original_url: 10,
            "https://info.cern.ch/hypertext/WWW/TheProject.html": 43,
            "http://line-mode.cern.ch/www/hypertext/WWW/TheProject.html": 43,
            "http://home.web.cern.ch/topics/birth-web": 103,
            "http://home.web.cern.ch/about": 121,
        }
        return url_result.get(str(url))

    mock_calculate_consumption_time.side_effect = calc_side_effect

    fake_html = b"""
    <html>
        <body>
            <a href="/hypertext/WWW/TheProject.html">Relative Link</a>
            <a href="http://line-mode.cern.ch/www/hypertext/WWW/TheProject.html">Absolute 1</a>
            <a href="http://home.web.cern.ch/topics/birth-web">Absolute 2</a>
            <a href="http://home.web.cern.ch/about">Absolute 3</a>
        </body>
    </html>
    """

    mock_response = MagicMock()
    mock_response.read.return_value = fake_html
    mock_response.__enter__.return_value = mock_response
    mock_urllib_request_urlopen.return_value = mock_response

    actual_result = runner.invoke(app, [original_url, "--depth", "1"])
    expected_exit_code = 0

    assert actual_result.exit_code == expected_exit_code
    assert "5m 20s" in actual_result.output
