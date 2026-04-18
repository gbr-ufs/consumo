# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/resolvers/file module."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from consumo.lib.exceptions import NoCacheError, UnsupportedMIMETypeError
from consumo.lib.resolvers.file import get_duration
from tests import FIXTURES_DIR


def test_get_duration_cache_hit() -> None:
    blog_post_html_consumption_time: int = 28
    mock_get_cached_resolver: Mock = Mock(return_value=blog_post_html_consumption_time)
    blog_post_html: Path = FIXTURES_DIR / "blog_post.html"

    actual_result: int = get_duration(
        blog_post_html, get_cached_resolver=mock_get_cached_resolver
    )
    expected_result: int = blog_post_html_consumption_time

    assert actual_result == expected_result


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


@patch("consumo.lib.resolvers.file.os.path.getmtime")
def test_get_duration_cache_result(mock_os_path_getmtime: Mock) -> None:
    audio_mp3: Path = FIXTURES_DIR / "audio.mp3"
    mock_os_path_getmtime.return_value = 1
    mock_get_cached_resolver: Mock = Mock(side_effect=NoCacheError)
    mock_cache_resolver: Mock = Mock()
    actual_result: int = get_duration(
        audio_mp3,
        get_cached_resolver=mock_get_cached_resolver,
        cache_resolver=mock_cache_resolver,
    )
    expected_result: int = 1

    assert mock_cache_resolver.called
    args: list[str] = mock_cache_resolver.call_args[0]
    assert args[0] == "consumo"
    assert args[1] == f"{str(audio_mp3.absolute)}:265"
    assert args[2] == expected_result
    assert args[3] == 1
    assert actual_result == expected_result


def test_get_duration_unsupported_mime_type_error(tmp_path: Path) -> None:
    mock_executable: Path = tmp_path / "executable"

    # Standard magic bytes for a Unix executable.
    mock_executable.write_bytes(
        b"\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )

    with pytest.raises(UnsupportedMIMETypeError):
        get_duration(mock_executable)


def test_get_duration_image() -> None:
    cool_png: Path = FIXTURES_DIR / "cool.png"
    actual_result: int = get_duration(cool_png)
    expected_result: int = 12

    assert actual_result == expected_result
