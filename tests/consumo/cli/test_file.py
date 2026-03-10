# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/file module."""

from pathlib import Path

from typer.testing import CliRunner, Result

from consumo.cli.file import app
from tests import FIXTURES_DIR

runner: CliRunner = CliRunner()


def test_process_file_get_multimedia_duration() -> None:
    actual_result: Result = runner.invoke(app, [str(FIXTURES_DIR / "audio.mp3")])
    expected_exit_code: int = 0
    expected_result: str = "1s"

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


def test_process_file_get_multimedia_duration_no_extension() -> None:
    actual_result: Result = runner.invoke(
        app, [str(FIXTURES_DIR / "audio_no_extension")]
    )
    expected_exit_code: int = 0
    expected_result: str = "1s"

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


def test_process_file_calculate_html_consumption_time() -> None:
    actual_result: Result = runner.invoke(app, [str(FIXTURES_DIR / "blog_post.html")])
    expected_exit_code: int = 0
    expected_result: str = "28s"

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


def test_process_file_calculate_viewing_time() -> None:
    actual_result: Result = runner.invoke(app, [str(FIXTURES_DIR / "cool.png")])
    expected_exit_code: int = 0
    expected_result: str = "12s"

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


def test_process_file_calculate_mass_media_consumption_time() -> None:
    actual_result: Result = runner.invoke(app, [str(FIXTURES_DIR / "empty.epub")])
    expected_exit_code: int = 0
    expected_result: str = "0s"

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


def test_process_file_unsupported_file_type(tmp_path: Path) -> None:
    mock_executable: Path = tmp_path / "executable"

    # Standard magic bytes for a Unix executable.
    mock_executable.write_bytes(
        b"\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )

    actual_result: Result = runner.invoke(app, [str(mock_executable)])
    expected_exit_code: int = 1
    expected_result: str = "Unsupported MIME type"

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


def test_process_file_directory_error() -> None:
    actual_result: Result = runner.invoke(app, [str(FIXTURES_DIR)])
    expected_exit_code: int = 1

    assert actual_result.exit_code == expected_exit_code
