# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/config module."""

from pathlib import Path

import pytest
from pydantic import NonNegativeInt
from pytest import CaptureFixture, MonkeyPatch

import consumo.cli.config as config
from consumo.cli.config import (
    load_configuration,
    set_default_value,
)


@pytest.fixture(autouse=True)
def reset_configuration_defaults() -> None:
    """Fixture to reset global configuration variables before each test."""
    config.DEFAULT_SORT = False
    config.DEFAULT_WORDS_PER_MINUTE = 265
    config.DEFAULT_SKIP_ERRORS = False
    config.DEFAULT_DEPTH = 0
    config.DEFAULT_CACHE = True


def test_load_configuration(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    config_file: Path = tmp_path / "config.toml"

    config_file.write_text("""
    [general]
    sort = true
    words_per_minute = 1000
    skip_errors = true
    [url]
    cache = false
    """)

    monkeypatch.setattr("typer.get_app_dir", lambda name: str(tmp_path))

    load_configuration()

    assert config.DEFAULT_SORT is True
    assert config.DEFAULT_WORDS_PER_MINUTE == 1000
    assert config.DEFAULT_SKIP_ERRORS is True
    assert config.DEFAULT_CACHE is False


def test_load_configuration_invalid_toml(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: CaptureFixture
) -> None:
    config_file: Path = tmp_path / "config.toml"

    config_file.write_text("""
    [general
    sort = true
    """)

    monkeypatch.setattr("typer.get_app_dir", lambda name: str(tmp_path))

    load_configuration()

    captured = capsys.readouterr()

    assert "Could not parse configuration file" in captured.out

    assert config.DEFAULT_SORT is False
    assert config.DEFAULT_WORDS_PER_MINUTE == 265


def test_set_default_value_interpretation_warning(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture
) -> None:
    monkeypatch.setenv("CONSUMO_WPM", "foo")
    actual_result: bool = set_default_value("CONSUMO_WPM", 265)
    expected_result: NonNegativeInt = 265
    expected_output: str = "Warning"

    captured = capsys.readouterr()

    assert expected_output in captured.out

    assert actual_result == expected_result


def test_set_default_value_boolean(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture
) -> None:
    monkeypatch.setenv("CONSUMO_SORT", "1")
    actual_result: bool = set_default_value("CONSUMO_SORT", False)
    expected_result: bool = True

    assert actual_result == expected_result
