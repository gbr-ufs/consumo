# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Core module for general consumption time processing."""

from consumo.lib.exceptions import NoCacheError


def dummy_get_cached_resolver(program_name: str, key: str) -> int:
    raise NoCacheError


def dummy_cache_resolver(
    program_name: str, key: str, value: int, time_to_live: int
) -> None:
    pass
