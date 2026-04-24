# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/config module."""

import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from pydantic import NonNegativeInt
from pytest import CaptureFixture, MonkeyPatch

import consumo.cli.config as config
from consumo.cli.config import (
    get_cache_directory,
    load_configuration,
    set_default_value,
)


@pytest.mark.parametrize(
    "platform, expected_suffix",
    [
        ("darwin", Path("Library/Caches/consumo")),
        ("win32", Path("AppData/Local/consumo/Cache")),
        ("linux", Path(".cache/consumo")),
    ],
)
@patch.dict("os.environ", {}, clear=True)
@patch("consumo.cli.config.Path.home")
@patch("consumo.cli.config.sys")
def test_get_cache_directory(
    mock_sys: Mock, mock_path_home: Mock, platform: str, expected_suffix: Path
) -> None:
    mock_sys.platform = platform

    mock_home: Path = Path("/home/mock")
    mock_path_home.return_value = mock_home

    actual_result: Path = get_cache_directory("consumo")
    expected_result: Path = mock_home / expected_suffix

    assert actual_result == expected_result


@patch("consumo.cli.config.sys")
def test_get_cache_directory_localappdata_set(mock_sys: Mock, tmp_path: Path) -> None:
    # Point LOCALAPPDATA to tmp_path.
    os.environ["LOCALAPPDATA"]: str = str(tmp_path)
    mock_sys.platform = "win32"

    actual_result: Path = get_cache_directory("consumo")
    expected_result: Path = tmp_path / "consumo" / "Cache"

    assert actual_result == expected_result


@patch("consumo.cli.config.sys")
def test_get_cache_directory_xdg_cache_set(mock_sys: Mock, tmp_path: Path) -> None:
    os.environ["XDG_CACHE_HOME"]: str = str(tmp_path)
    mock_sys.platform = "linux"

    actual_result: Path = get_cache_directory("consumo")
    expected_result: Path = tmp_path / "consumo"

    assert actual_result == expected_result


@pytest.fixture(autouse=True)
def reset_configuration_defaults() -> None:
    """Fixture to reset global configuration variables before each test."""
    config.DEFAULT_SORT = False
    config.DEFAULT_WORDS_PER_MINUTE = 265
    config.DEFAULT_SKIP_ERRORS = False
    config.DEFAULT_DEPTH = 0
    config.DEFAULT_CACHE = True


def test_load_configuration(tmp_path: Path) -> None:
    config_file: Path = tmp_path / "config.toml"

    config_file.write_text("""
    [general]
    sort = true
    words_per_minute = 1000
    skip_errors = true
    [url]
    cache = false
    """)

    load_configuration(config_file)

    assert config.DEFAULT_SORT is True
    assert config.DEFAULT_WORDS_PER_MINUTE == 1000
    assert config.DEFAULT_SKIP_ERRORS is True
    assert config.DEFAULT_CACHE is False


def test_load_configuration_invalid_toml(
    tmp_path: Path, capsys: CaptureFixture
) -> None:
    config_file: Path = tmp_path / "config.toml"

    config_file.write_text("""
    [general
    sort = true
    """)

    load_configuration(config_file)

    captured = capsys.readouterr()

    assert "Could not parse configuration file" in captured.out

    assert config.DEFAULT_SORT is False
    assert config.DEFAULT_WORDS_PER_MINUTE == 265


def test_load_configuration_file_not_found(tmp_path: Path) -> None:
    non_existent_file: Path = tmp_path / "does_not_exist.toml"

    load_configuration(non_existent_file)


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
