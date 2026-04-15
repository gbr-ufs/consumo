# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/file module."""

from coverage.files import abs_file

from pathlib import Path
from sqlite3 import OperationalError
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner, Result

from consumo.cli.file import app, get_duration
from consumo.lib.exceptions import UnsupportedMIMETypeError
from tests import FIXTURES_DIR

runner: CliRunner = CliRunner()


@pytest.mark.parametrize(
    "filename, expected_exit_code, expected_result",
    [
        ("audio.mp3", 0, "1s"),
        ("audio_no_extension", 0, "1s"),
        ("blog_post.html", 0, "28s"),
        ("cool.png", 0, "12s"),
        ("empty.epub", 0, "0s"),
    ],
    ids=[
        "get_multimedia_duration",
        "get_multimedia_duration_no_extension",
        "calculate_html_consumption_time",
        "calculate_viewing_time",
        "calculate_mass_media_consumption_time",
    ],
)
def test_process_files_get_standard_files(
    filename: str, expected_exit_code: int, expected_result: str
) -> None:
    actual_result: Result = runner.invoke(app, [str(FIXTURES_DIR / filename)])

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


def test_process_files_unsupported_file_type(tmp_path: Path) -> None:
    mock_executable: Path = tmp_path / "executable"

    # Standard magic bytes for a Unix executable.
    mock_executable.write_bytes(
        b"\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )

    with pytest.raises(UnsupportedMIMETypeError):
        runner.invoke(app, [str(mock_executable)], catch_exceptions=False)


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


def test_get_duration_cache_result() -> None:
    audio_mp3: Path = FIXTURES_DIR / "audio.mp3"
    mock_get_cached_resolver: Mock = Mock(side_effect=OperationalError)
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
    assert args[1] == str(audio_mp3.absolute)
    assert args[2] == expected_result
    assert args[3] == 1773603896.6067152
    assert actual_result == expected_result
