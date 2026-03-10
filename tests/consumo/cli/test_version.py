# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/version module."""

from typer.testing import CliRunner, Result

from consumo.__init__ import __version__ as expected_result
from consumo.cli.version import app

runner: CliRunner = CliRunner()


def test_version() -> None:
    actual_result: Result = runner.invoke(app)
    expected_exit_code: int = 0

    assert actual_result.exit_code == expected_exit_code
    assert expected_result in actual_result.output
