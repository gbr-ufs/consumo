# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/cache module."""

from pathlib import Path

import pytest
from pytest import MonkeyPatch

from consumo.cli.cache import cache_result, get_cached_result
from consumo.lib.exceptions import NoCacheError


def test_cache_result_and_get_cached_result(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    cache_dir: Path = tmp_path / "consumo"
    # 1 day in seconds.
    time_to_live: int = 86400

    # Write a value.
    cache_result(cache_dir, "https://example.com", 1278, time_to_live)

    # Read it back.
    actual_result: int = get_cached_result(cache_dir, "https://example.com")
    expected_result: int = 1278

    assert actual_result == expected_result

    cache_result(cache_dir, "https://example.com", 1278, -1)

    # Read it back after expiration.
    with pytest.raises(
        NoCacheError,
    ):
        actual_result: int = get_cached_result(cache_dir, "https://example.com")

    # Read non-existent key.
    with pytest.raises(NoCacheError):
        actual_result: int = get_cached_result(cache_dir, "https://example.org")

    # Inaccessible database path.
    with pytest.raises(NoCacheError):
        actual_result: int = get_cached_result(
            Path("/root/bogus"), "https://example.com"
        )
