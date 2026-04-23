# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/file module."""

from unittest.mock import Mock, patch

from pydantic import HttpUrl
from typer.testing import CliRunner, Result

from consumo.cli.file import app
from tests import FIXTURES_DIR

runner: CliRunner = CliRunner()


@patch("consumo.lib.file.html.get_absolute_path_multimedia_duration")
def test_app(mock_get_absolute_path_multimedia_duration: Mock) -> None:
    mock_get_absolute_path_multimedia_duration.return_value = 5713

    audio_mp3: str = str(FIXTURES_DIR / "audio.mp3")
    cool_png: str = str(FIXTURES_DIR / "cool.png")
    single_char_pdf: str = str(FIXTURES_DIR / "single_char.pdf")
    text_txt: str = str(FIXTURES_DIR / "text.txt")
    url_html: str = str(FIXTURES_DIR / "url.html")
    args: list[str] = [
        audio_mp3,
        cool_png,
        single_char_pdf,
        text_txt,
        url_html,
        "--sort",
    ]
    actual_result: Result = runner.invoke(app, args)
    expected_exit_code: int = 0
    expected_results: list[str] = ["1s", "1s", "6s", "12s", "1h 37m 11s"]

    assert actual_result.exit_code == expected_exit_code

    for expected_result in expected_results:
        assert expected_result in actual_result.output
