# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/resolvers/url module."""

from unittest.mock import MagicMock, Mock, patch

import pytest
from av.error import FFmpegError
from pydantic import HttpUrl, NonNegativeInt

from consumo.lib.exceptions import NoCacheError
from consumo.lib.resolvers.url import get_duration


class FakeDate:
    @staticmethod
    def today():
        # Fixed date for assertions.
        from datetime import date

        return date(2026, 3, 27)


@pytest.mark.parametrize(
    "url, expected_result",
    [
        (
            "https://dn710704.ca.archive.org/0/items/night_of_the_living_dead_dvd/Night.mp4",
            5732,
        )
    ],
)
@patch("consumo.lib.resolvers.url.get_multimedia_duration")
@patch("consumo.lib.resolvers.url.get_hosted_multimedia_duration")
def test_get_duration_not_hosted(
    mock_get_hosted_multimedia_duration: Mock,
    mock_get_multimedia_duration: Mock,
    url: HttpUrl,
    expected_result: int,
) -> None:
    mock_get_hosted_multimedia_duration.side_effect = FFmpegError(0, "", "")
    mock_get_multimedia_duration.return_value = expected_result
    actual_result: int = get_duration(url, cache=False)

    assert actual_result == expected_result


@pytest.mark.parametrize(
    "url, expected_result",
    [("https://www.youtube.com/watch?v=H91BxkBXttE", 5717)],
)
@patch("consumo.lib.resolvers.url.get_hosted_multimedia_duration")
@patch("consumo.lib.resolvers.url.date", new=FakeDate)
def test_get_duration_hosted(
    mock_get_hosted_multimedia_duration: Mock,
    url: HttpUrl,
    expected_result: int,
) -> None:
    mock_get_cached_resolver: Mock = Mock(side_effect=NoCacheError)
    mock_cache_resolver: Mock = Mock()
    mock_get_hosted_multimedia_duration.return_value = expected_result
    actual_result: int = get_duration(
        HttpUrl(url),
        get_cached_resolver=mock_get_cached_resolver,
        cache_resolver=mock_cache_resolver,
    )

    assert mock_cache_resolver.called
    args: list[str] = mock_cache_resolver.call_args[0]
    assert args[0] == "consumo"
    assert args[1] == f"{url}:265:0"
    assert args[2] == expected_result
    assert args[3] == "2026-03-27"
    assert actual_result == expected_result


def test_get_duration_cache_hit() -> None:
    mock_get_cached_resolver: Mock = Mock(return_value=43)

    actual_result: int = get_duration(
        HttpUrl("https://info.cern.ch/hypertext/WWW/TheProject.html"),
        get_cached_resolver=mock_get_cached_resolver,
    )
    expected_result: int = 43

    assert actual_result == expected_result


@patch("consumo.lib.resolvers.url.calculate_consumption_time")
@patch("consumo.lib.resolvers.url.get_multimedia_duration")
@patch("consumo.lib.resolvers.url.date", new=FakeDate)
def test_get_duration_hosted_success_and_cached(
    mock_get_multimedia_duration: Mock,
    mock_calculate_consumption_time: Mock,
) -> None:
    mock_get_cached_resolver: Mock = Mock(side_effect=NoCacheError)
    mock_get_multimedia_duration.side_effect = FFmpegError(0, "", "")
    mock_cache_resolver: Mock = Mock()
    mock_calculate_consumption_time.return_value = 43

    actual_result: int = get_duration(
        HttpUrl("https://info.cern.ch/hypertext/WWW/TheProject.html"),
        get_cached_resolver=mock_get_cached_resolver,
        cache_resolver=mock_cache_resolver,
    )
    expected_result: int = 43

    assert actual_result == expected_result


@pytest.mark.parametrize(
    "url, expected_result",
    [("https://www.youtube.com/watch?v=H91BxkBXttE", 5717)],
)
@patch("consumo.lib.resolvers.url.get_hosted_multimedia_duration")
def test_get_duration_hosted_no_cache(
    mock_get_hosted_multimedia_duration: Mock,
    url: HttpUrl,
    expected_result: int,
) -> None:
    mock_get_hosted_multimedia_duration.return_value = expected_result
    actual_result: int = get_duration(HttpUrl(url), cache=False)

    assert actual_result == expected_result


@patch("consumo.lib.resolvers.url.urllib.request.urlopen")
@patch("consumo.lib.resolvers.url.calculate_consumption_time")
@patch("consumo.lib.resolvers.url.get_multimedia_duration")
def test_get_duration_depth(
    mock_get_multimedia_duration: Mock,
    mock_calculate_consumption_time: Mock,
    mock_urllib_request_urlopen: Mock,
) -> None:
    original_url: HttpUrl = HttpUrl("https://info.cern.ch/")
    mock_get_multimedia_duration.side_effect = FFmpegError(1, "", "")

    def calculate_consumption_time_side_effect(
        url: HttpUrl, words_per_minute: NonNegativeInt = 265
    ) -> int:
        url_result: dict[str, int] = {
            str(original_url): 10,
            "https://info.cern.ch/hypertext/WWW/TheProject.html": 43,
            "http://line-mode.cern.ch/www/hypertext/WWW/TheProject.html": 43,
            "http://home.web.cern.ch/topics/birth-web": 103,
            "http://home.web.cern.ch/about": 121,
        }

        return url_result[str(url)]

    mock_calculate_consumption_time.side_effect = calculate_consumption_time_side_effect

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

    mock_response: MagicMock = MagicMock()
    mock_response.read.return_value = fake_html
    mock_response.__enter__.return_value = mock_response
    mock_urllib_request_urlopen.return_value = mock_response

    actual_result: int = get_duration(original_url, depth=1)
    expected_result: int = 320

    assert actual_result == expected_result
