# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/file/multimedia module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import HttpUrl

from consumo.lib.exceptions import MissingMetadataError
from consumo.lib.file.multimedia import (
    get_duration,
    get_multimedia_duration,
    duration_resolver,
)
from tests import FIXTURES_DIR


@pytest.mark.parametrize(
    "url, expected_duration",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", 213),
        (
            "https://www.youtube.com/playlist?list=OLAK5uy_mh1h77B5MWPheIzdy3mA_PtEr8yC-JorI",
            4330,
        ),
        (
            "https://dn710704.ca.archive.org/0/items/night_of_the_living_dead_dvd/Night.mp4",
            5732,
        ),
    ],
)
@patch("consumo.lib.file.multimedia.av.open")
@patch("consumo.lib.file.multimedia.YoutubeDL")
def test_get_duration(
    mock_ytdl: MagicMock, mock_av_open: MagicMock, url: str, expected_duration: int
) -> None:
    if (
        url
        == "https://www.youtube.com/playlist?list=OLAK5uy_mh1h77B5MWPheIzdy3mA_PtEr8yC-JorI"
    ):
        mock_ytdl.return_value.__enter__.return_value.extract_info.return_value: dict[
            str, int
        ] = {
            "entries": [
                {"duration": 1360},
                {"duration": 1270},
                {"duration": 710},
                {"duration": 990},
            ]
        }
    else:
        mock_ytdl.return_value.__enter__.return_value.extract_info.return_value: dict[
            str, int
        ] = {"duration": expected_duration}
    mock_av_open.return_value.__enter__.return_value.duration = 5731831832
    actual_duration: int = get_duration(HttpUrl(url))

    assert actual_duration == expected_duration


def test_get_multimedia_duration_missingmetadataerror() -> None:
    video_no_duration_h264: Path = FIXTURES_DIR / "video_no_duration.h264"

    with pytest.raises(MissingMetadataError):
        get_multimedia_duration(video_no_duration_h264)


def test_duration_resolver_missingmetadataerror() -> None:
    with pytest.raises(MissingMetadataError):
        duration_resolver({"duration": None})
