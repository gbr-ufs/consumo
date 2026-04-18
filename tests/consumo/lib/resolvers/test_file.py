# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/resolvers/file module."""

from pathlib import Path
from unittest.mock import Mock

import pytest

from consumo.lib.exceptions import UnsupportedMIMETypeError
from consumo.lib.resolvers.file import get_duration
from tests import FIXTURES_DIR


def test_get_duration_cache_hit() -> None:
    url_html_consumption_time: int = 5831
    mock_get_cached_resolver: Mock = Mock(return_value=url_html_consumption_time)
    url_html: Path = FIXTURES_DIR / "url.html"

    actual_result: int = get_duration(
        url_html, get_cached_resolver=mock_get_cached_resolver
    )

    assert actual_result == url_html_consumption_time


def test_get_duration_no_cache() -> None:
    single_char_pdf: Path = FIXTURES_DIR / "single_char.pdf"
    actual_result: int = get_duration(single_char_pdf, cache=False)
    expected_result: int = 1

    assert actual_result == expected_result


def test_get_duration_no_cache_multimedia() -> None:
    audio_mp3: Path = FIXTURES_DIR / "audio.mp3"
    actual_result: int = get_duration(audio_mp3, cache=False)
    expected_result: int = 1

    assert actual_result == expected_result


def test_get_duration_unsupported_mime_type_error(tmp_path: Path) -> None:
    mock_executable: Path = tmp_path / "executable"

    # Standard magic bytes for a Unix executable.
    mock_executable.write_bytes(
        b"\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )

    with pytest.raises(UnsupportedMIMETypeError):
        get_duration(mock_executable)
