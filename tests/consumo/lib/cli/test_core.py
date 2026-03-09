# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import Mock, patch

from pytest import CaptureFixture, MonkeyPatch

from consumo.cli.state import configuration
from consumo.lib.cli.core import execute_concurrent_command
from consumo.lib.types import Second


@patch("consumo.lib.cli.core.handle_multiple_args")
def test_execute_concurrent_command_sorted(
    handle_multiple_args: Mock,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture,
) -> None:
    monkeypatch.setattr(configuration, "sort", True)
    handle_multiple_args.return_value: dict[str, Second] = {
        "https://info.cern.ch/hypertext/WWW/TheProject.html": 43,
        "https://dn710704.ca.archive.org/0/items/night_of_the_living_dead_dvd/Night.mp4": 5732,
        "https://www.bbc.com/news/articles/c4g0dzg6e4mo": 297,
    }

    mock_args: list[str] = list(handle_multiple_args.return_value.keys())
    resolver: Mock = Mock()

    execute_concurrent_command(mock_args, resolver)

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
