# SPDX-License-Identifier: GPL-3.0-or-later

"""Core module for general consumption time processing."""

from consumo.lib.exceptions import NoCacheError


def dummy_get_cached_resolver(program_name: str, key: str, current_time: float) -> int:
    raise NoCacheError


def dummy_cache_resolver(
    program_name: str, key: str, value: int, current_time: float
) -> None:
    pass
