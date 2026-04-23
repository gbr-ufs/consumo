# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/core module."""

from unittest.mock import Mock, patch

from pytest import CaptureFixture, MonkeyPatch

from consumo.cli.core import execute_concurrent_command


@patch("consumo.cli.core.handle_multiple_args")
def test_execute_concurrent_command(
    mock_handle_multiple_args: Mock,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture,
) -> None:
    mock_handle_multiple_args.return_value = (
        {
            "https://info.cern.ch/hypertext/WWW/TheProject.html": 43,
        },
        {},
    )

    mock_args = list(mock_handle_multiple_args.return_value[0].keys())
    duration_resolver: Mock = Mock()

    execute_concurrent_command(mock_args, duration_resolver)

    captured = capsys.readouterr()

    output_lines: list[str] = [
        line for line in captured.out.split("\n") if line.strip()
    ]

    assert len(output_lines) == 1
    assert "43s" in output_lines[0]
