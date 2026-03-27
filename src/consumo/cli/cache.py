# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for working with consumo's cache system."""

import os
import sqlite3
import sys
from pathlib import Path
from sqlite3 import Cursor
from typing import Optional


def get_cache_directory(program_name: str) -> Path:
    """Get the program's cache directory on the system.

    Args:
        program_name: The name of the program whose cache path directory will
            be resolved.

    Returns:
        The path to the cache directory of the program on the current system.
    """
    home: Path = Path.home()

    if sys.platform == "darwin":
        return home / "Library" / "Caches" / program_name

    elif sys.platform == "win32":
        local_app_data: str | None = os.getenv("LOCALAPPDATA")

        if local_app_data:
            base_directory: Path = Path(local_app_data)
        else:
            base_directory: Path = home / "AppData" / "Local"
        return base_directory / program_name / "Cache"

    # Unix-like.
    xdg_cache: str | None = os.getenv("XDG_CACHE_HOME")

    if xdg_cache:
        base_directory = Path(xdg_cache)
    else:
        base_directory = home / ".cache"

    return base_directory / program_name


def cache_result(program_name: str, key: str, time: int | float, value: int) -> None:
    """Store CLI result on cache.

    The cache is implemented as SQLite database because it is serverless.

    Args:
        program_name: The name of the CLI program whose result will be cached.
        key: The input that was given to the program whose result will now be
            cached.
        time: The current time for cache invalidation in the future.
        value: The result given by the program.
    """
    cache_directory: Path = get_cache_directory(program_name)

    cache_directory.mkdir(exist_ok=True)

    database_path: Path = cache_directory / f"{program_name}.db"

    with sqlite3.connect(database_path, autocommit=True) as connection:
        cursor: Cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY,
            time REAL NOT NULL, value INTEGER NOT NULL)
            """
        )
        cursor.execute(
            "INSERT OR REPLACE INTO cache (key, time, value) VALUES (?, ?, ?)",
            (key, time, value),
        )


def get_cached_result(
    program_name: str, key: str, current_time: int | float
) -> int | None:
    """Get CLI result stored on cache.

    The cache is implemented as SQLite database because it is serverless.

    Args:
        key: The key to search for in the database to look for a stored value.
        current_time: The time when this function was called for cache
            validation. If this time is generally in line with the one on the
            database, then the value is returned.

    Returns:
        The integer value corresponding to the key in the database. Returns
        None if nothing was found.
    """
    cache_directory: Path = get_cache_directory(program_name)
    database_path: Path = cache_directory / f"{program_name}.db"

    with sqlite3.connect(database_path) as connection:
        cursor: Cursor = connection.cursor()

        cursor.execute(
            """
            SELECT time, value FROM cache WHERE key = ?""",
            (key,),
        )

        row: tuple[int | float, int] | None = cursor.fetchone()

        if row is None:
            return row

        cached_time, cached_value = row

        if current_time == cached_time:
            return cached_value
