# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Core module for general consumption time processing."""

from pathlib import Path

from consumo.lib.exceptions import NoCacheError


def dummy_get_cached_resolver(cache_dir: Path, key: str) -> int:
    raise NoCacheError


def dummy_cache_resolver(
    cache_dir: Path, key: str, value: int, time_to_live: int
) -> None:
    pass
