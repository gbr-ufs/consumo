# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/file module."""

from pathlib import Path

from pytest import mark
from typer.testing import CliRunner, Result

from consumo.cli.file import app
from tests import FIXTURES_DIR

runner: CliRunner = CliRunner()


@mark.parametrize(
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
def test_process_file_get_standard_files(
    filename: str, expected_exit_code: int, expected_result: str
) -> None:
    actual_result: Result = runner.invoke(app, [str(FIXTURES_DIR / filename)])

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
