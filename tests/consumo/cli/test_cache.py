# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/cache module."""

import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from pytest import MonkeyPatch

from consumo.cli.cache import cache_result, get_cache_directory, get_cached_result
from consumo.lib.exceptions import NoCacheError


@pytest.mark.parametrize(
    "platform, expected_suffix",
    [
        ("darwin", Path("Library/Caches/consumo")),
        ("win32", Path("AppData/Local/consumo/Cache")),
        ("linux", Path(".cache/consumo")),
    ],
)
@patch.dict("os.environ", {}, clear=True)
@patch("consumo.cli.cache.Path.home")
@patch("consumo.cli.cache.sys")
def test_get_cache_directory(
    mock_sys: Mock, mock_path_home, platform: str, expected_suffix: Path
) -> None:
    mock_sys.platform = platform

    mock_home: Path = Path("/home/mock")
    mock_path_home.return_value = mock_home

    actual_result: Path = get_cache_directory("consumo")
    expected_result: Path = mock_home / expected_suffix

    assert actual_result == expected_result


@patch("consumo.cli.cache.sys")
def test_get_cache_directory_localappdata_set(mock_sys: Mock, tmp_path: Path) -> None:
    # Point LOCALAPPDATA to tmp_path.
    os.environ["LOCALAPPDATA"]: str = str(tmp_path)
    mock_sys.platform = "win32"

    actual_result: Path = get_cache_directory("consumo")
    expected_result: Path = tmp_path / "consumo" / "Cache"

    assert actual_result == expected_result


@patch("consumo.cli.cache.sys")
def test_get_cache_directory_xdg_cache_set(mock_sys: Mock, tmp_path: Path) -> None:
    os.environ["XDG_CACHE_HOME"]: str = str(tmp_path)
    mock_sys.platform = "linux"

    actual_result: Path = get_cache_directory("consumo")
    expected_result: Path = tmp_path / "consumo"

    assert actual_result == expected_result


@patch("consumo.cli.cache.get_cache_directory")
def test_cache_result_and_get_cached_result_roundtrip(
    mock_get_cache_directory: Mock, monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    mock_get_cache_directory.return_value = tmp_path
    # 1 day in seconds.
    time_to_live: int = 86400

    # Write a value.
    cache_result("consumo", "https://example.com", 1278, time_to_live)

    # Read it back.
    actual_result: int = get_cached_result("consumo", "https://example.com")
    expected_result: int = 1278

    assert actual_result == expected_result

    cache_result("consumo", "https://example.com", 1278, -1)

    # Read it back after expiration.
    with pytest.raises(
        NoCacheError,
    ):
        actual_result: int = get_cached_result("consumo", "https://example.com")

    # Read non-existent key.
    with pytest.raises(NoCacheError):
        actual_result: int = get_cached_result("consumo", "https://example.org")

    mock_get_cache_directory.return_value = Path("/root/bogus")

    # Inaccessible database path.
    with pytest.raises(NoCacheError):
        actual_result: int = get_cached_result("consumo", "https://example.com")
