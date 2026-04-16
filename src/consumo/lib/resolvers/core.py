# SPDX-License-Identifier: GPL-3.0-or-later

"""Core module for general consumption time processing."""

from sqlite3 import OperationalError


def dummy_get_cached_resolver(program_name: str, key: str, current_time: float) -> int:
    raise OperationalError


def dummy_cache_resolver(
    program_name: str, key: str, value: int, current_time: float
) -> None:
    pass
