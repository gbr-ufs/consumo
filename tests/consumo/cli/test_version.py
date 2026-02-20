# SPDX-License-Identifier: GPL-3.0-or-later


from typer.testing import CliRunner, Result

from consumo.__init__ import __version__ as expected_version
from consumo.cli.version import app

runner: CliRunner = CliRunner()


def test_version() -> None:
    actual_version: Result = runner.invoke(app)
    expected_exit_code: int = 0

    assert actual_version.exit_code == expected_exit_code
    assert expected_version in actual_version.output
