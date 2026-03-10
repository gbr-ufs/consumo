# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/config module."""

from pathlib import Path

import pytest

import consumo.cli.config as config


@pytest.fixture(autouse=True)
def reset_config_defaults() -> None:
    """Fixture to reset global configuration variables before each test."""
    config.DEFAULT_SORT = False
    config.DEFAULT_WORDS_PER_MINUTE = 265


def test_load_configuration_valid(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_file: Path = tmp_path / "config.toml"

    config_file.write_text("""
    [general]
    sort = true
    words_per_minute = 1000
    """)

    monkeypatch.setattr("typer.get_app_dir", lambda name: str(tmp_path))

    config.load_configuration()

    assert config.DEFAULT_SORT is True
    assert config.DEFAULT_WORDS_PER_MINUTE == 1000


def test_load_configuration_missing_sort(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_file: Path = tmp_path / "config.toml"

    config_file.write_text("""
    [general]
    words_per_minute = 1000
    """)

    monkeypatch.setattr("typer.get_app_dir", lambda name: str(tmp_path))

    config.load_configuration()

    assert config.DEFAULT_SORT is False
    assert config.DEFAULT_WORDS_PER_MINUTE == 1000


def test_load_configuration_missing_words_per_minute(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_file: Path = tmp_path / "config.toml"

    config_file.write_text("""
    [general]
    sort = true
    """)

    monkeypatch.setattr("typer.get_app_dir", lambda name: str(tmp_path))

    config.load_configuration()

    assert config.DEFAULT_SORT is True
    assert config.DEFAULT_WORDS_PER_MINUTE == 265


def test_load_configuration_invalid_toml(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    config_file: Path = tmp_path / "config.toml"

    config_file.write_text("""
    [general
    sort = true
    """)

    monkeypatch.setattr("typer.get_app_dir", lambda name: str(tmp_path))

    config.load_configuration()

    captured = capsys.readouterr()

    assert "Could not parse configuration file" in captured.out

    assert config.DEFAULT_SORT is False
    assert config.DEFAULT_WORDS_PER_MINUTE == 265


def test_load_configuration_missing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("typer.get_app_dir", lambda name: str(tmp_path))

    config.load_configuration()

    assert config.DEFAULT_SORT is False
    assert config.DEFAULT_WORDS_PER_MINUTE == 265
