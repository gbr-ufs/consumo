# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for working with consumo's cache system."""

import os
import sqlite3
import sys
import time
from pathlib import Path
from sqlite3 import Cursor, OperationalError

from consumo.lib.exceptions import NoCacheError


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


def cache_result(program_name: str, key: str, value: int, time_to_live: int) -> None:
    """Store CLI result on cache.

    The cache is implemented as a SQLite database because it is serverless.

    Args:
        program_name: The name of the CLI program whose result will be cached.
        key: The input that was given to the program whose result will now be
            cached.
        value: The result given by the program.
        time_to_live: How many seconds this cache entry should remain valid.
    """
    cache_directory: Path = get_cache_directory(program_name)

    cache_directory.mkdir(exist_ok=True, parents=True)

    database_path: Path = cache_directory / f"{program_name}.db"

    expires_at: int | float = time.time() + time_to_live

    with sqlite3.connect(database_path, autocommit=True) as connection:
        cursor: Cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            cache (
            key TEXT PRIMARY KEY,
            value INTEGER NOT NULL,
            expires_at REAL NOT NULL
            )
            """
        )
        cursor.execute(
            """INSERT OR REPLACE INTO
            cache (
            key,
            value,
            expires_at
            )
            VALUES (?, ?, ?)""",
            (key, value, expires_at),
        )


def get_cached_result(program_name: str, key: str) -> int:
    """Get CLI result stored on cache.

    The cache is implemented as a SQLite database because it is serverless.

    Args:
        program_name: The name of the CLI program whose result will be returned.
        key: The key to search for in the database.

    Returns:
        The integer value corresponding to the key in the database.
    """
    cache_directory: Path = get_cache_directory(program_name)
    database_path: Path = cache_directory / f"{program_name}.db"
    current_time: int | float = time.time()

    try:
        with sqlite3.connect(database_path) as connection:
            cursor: Cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                value
                FROM
                cache
                WHERE
                key = ?
                AND
                expires_at > ?
                """,
                (key, current_time),
            )

            row: tuple[int] | None = cursor.fetchone()

            if row is None:
                raise NoCacheError("Value not found")

            return row[0]
    except OperationalError:
        raise NoCacheError("Unable to open database file")
