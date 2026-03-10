# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/core module."""

from unittest.mock import Mock, patch

from pytest import CaptureFixture, MonkeyPatch

from consumo.cli.core import execute_concurrent_command
from consumo.lib.types import Second


@patch("consumo.cli.core.handle_multiple_args")
def test_execute_concurrent_command_sorted(
    mock_handle_multiple_args: Mock,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture,
) -> None:
    mock_handle_multiple_args.return_value: dict[str, Second] = {
        "https://info.cern.ch/hypertext/WWW/TheProject.html": 43,
        "https://dn710704.ca.archive.org/0/items/night_of_the_living_dead_dvd/Night.mp4": 5732,
        "https://www.bbc.com/news/articles/c4g0dzg6e4mo": 297,
    }

    mock_args: list[str] = list(mock_handle_multiple_args.return_value.keys())
    duration_resolver: Mock = Mock()

    execute_concurrent_command(mock_args, duration_resolver, sort=True)

    captured = capsys.readouterr()

    # Split the output by line and remove any empty trailing lines.
    output_lines: list[str] = [
        line for line in captured.out.split("\n") if line.strip()
    ]

    # Assert the printed lines are sorted.
    assert len(output_lines) == 3
    assert "https://info.cern.ch/hypertext/WWW/TheProject.html # 43s" in output_lines[0]
    assert "https://www.bbc.com/news/articles/c4g0dzg6e4mo # 4m 57s" in output_lines[1]
    assert (
        "https://dn710704.ca.archive.org/0/items/night_of_the_living_dead_dvd/Night.mp4 # 1h 35m 32s"
        in output_lines[2]
    )
