# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/url module."""

from unittest.mock import Mock, patch

from typer.testing import CliRunner, Result

from consumo.cli.url import app

runner: CliRunner = CliRunner()


@patch("consumo.cli.url.get_duration")
def test_app(mock_get_duration: Mock) -> None:
    mock_get_duration.return_value = 5732

    actual_result: Result = runner.invoke(
        app,
        [
            "https://dn710704.ca.archive.org/0/items/night_of_the_living_dead_dvd/Night.mp4"
        ],
    )
    expected_exit_code: int = 0
    expected_result: str = "1h 35m 32s"

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output


@patch("consumo.cli.url.get_duration")
def test_app_skip_errors(mock_get_duration: Mock) -> None:
    mock_get_duration.return_value = 5732

    actual_result: Result = runner.invoke(
        app,
        [
            "https://dn710704.ca.archive.org/0/items/night_of_the_living_dead_dvd/Night.mp4",
            "LICENSE",
            "--skip-errors",
        ],
    )
    expected_exit_code: int = 0
    expected_result: str = "1h 35m 32s"
    expected_error: str = "ValidationError"

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output
    assert expected_error in actual_result.output
