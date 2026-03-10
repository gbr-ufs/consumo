# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/list module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner, Result

from consumo.cli.list import app
from tests import FIXTURES_DIR

runner: CliRunner = CliRunner()


@patch("consumo.cli.core.handle_multiple_args")
def test_process_list(mock_handle_multiple_args: MagicMock) -> None:
    mock_handle_multiple_args.return_value = {
        "https://github.com/gbr-ufs/pf": 13,
        "https://github.com/gbr-ufs/cses": 4,
        "https://github.com/gbr-ufs/notes": 16,
        "https://github.com/gbr-ufs/ies": 21,
        "https://github.com/gbr-ufs/hack-ia-mockup": 31,
        "https://github.com/gbr-ufs/probabilidade-detran-se": 14,
        "https://github.com/gbr-ufs/hello-r-markdown": 4,
    }
    actual_result: Result = runner.invoke(app, [str(FIXTURES_DIR / "links.txt")])
    expected_exit_code: int = 0
    expected_results: list[str] = ["13s", "4s", "16s", "21s", "31s", "14s", "4s"]

    assert actual_result.exit_code == expected_exit_code
    for expected_result in expected_results:
        assert expected_result in actual_result.output


def test_process_list_unsupported_file_type(tmp_path: Path) -> None:
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


def test_process_list_directory_error() -> None:
    actual_result: Result = runner.invoke(app, [str(FIXTURES_DIR)])
    expected_exit_code: int = 1

    assert actual_result.exit_code == expected_exit_code
