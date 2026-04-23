# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/handlers/url module."""

from unittest.mock import Mock, patch

from av.error import FFmpegError
from pydantic import HttpUrl

from consumo.lib.handlers.url import get_duration


def test_get_duration_cache_hit() -> None:
    mock_get_cached_resolver: Mock = Mock(return_value=43)

    actual_result: int = get_duration(
        HttpUrl("https://info.cern.ch/hypertext/WWW/TheProject.html"),
        get_cached_resolver=mock_get_cached_resolver,
    )
    expected_result: int = 43

    assert actual_result == expected_result


@patch("consumo.lib.handlers.url.get_hosted_multimedia_duration")
def test_get_duration_hosted_no_cache(
    mock_get_hosted_multimedia_duration: Mock,
) -> None:
    url: HttpUrl = HttpUrl("https://www.youtube.com/watch?v=H91BxkBXttE")
    expected_result: int = 5717
    mock_get_hosted_multimedia_duration.return_value = expected_result
    actual_result: int = get_duration(HttpUrl(url), cache=False)

    assert actual_result == expected_result


@patch("consumo.lib.handlers.url.calculate_consumption_time")
@patch("consumo.lib.handlers.url.get_multimedia_duration")
def test_get_duration_not_hosted_no_cache(
    mock_get_multimedia_duration: Mock, mock_calculate_consumption_time: Mock
) -> None:
    expected_result: int = 43
    mock_get_multimedia_duration.side_effect = FFmpegError(0, "", "")
    mock_calculate_consumption_time.return_value = expected_result
    actual_result: int = get_duration(
        HttpUrl("https://info.cern.ch/hypertext/WWW/TheProject.html"), cache=False
    )

    assert actual_result == expected_result
