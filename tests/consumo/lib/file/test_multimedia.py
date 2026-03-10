# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/file/multimedia module."""

import pytest
from pydantic import FilePath
from pytest import mark

from consumo.lib.exceptions import MissingMetadataError
from consumo.lib.file.multimedia import get_duration
from consumo.lib.types import Second
from tests import FIXTURES_DIR


@mark.parametrize(
    "filename, expected_duration",
    [
        ("audio.mp3", 1),
        ("video.mkv", 1),
        ("audio_no_extension", 1),
    ],
)
def test_get_duration(filename: str, expected_duration: Second) -> None:
    container: FilePath = FIXTURES_DIR / filename
    actual_duration: Second = get_duration(container)

    assert actual_duration == expected_duration


def test_get_duration_no_duration() -> None:
    with pytest.raises(MissingMetadataError):
        container: FilePath = FIXTURES_DIR / "video_no_duration.h264"

        get_duration(container)
