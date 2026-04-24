# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for working with consumo's cache system."""

import sqlite3
import time
from pathlib import Path
from sqlite3 import Cursor, OperationalError

from consumo.lib.exceptions import NoCacheError


def cache_result(cache_dir: Path, key: str, value: int, time_to_live: int) -> None:
    """Store CLI result on cache.

    The cache is implemented as a SQLite database because it is serverless.

    Args:
        cache_dir: The path to where the cache will be stored.
        key: The input that was given to the program whose result will now be
            cached.
        value: The result given by the program.
        time_to_live: How many seconds this cache entry should remain valid.
    """
    cache_dir.mkdir(exist_ok=True, parents=True)
    database_file: Path = cache_dir / "consumo.db"

    expires_at: int | float = time.time() + time_to_live

    with sqlite3.connect(database_file, autocommit=True) as connection:
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


def get_cached_result(cache_dir: Path, key: str) -> int:
    """Get CLI result stored on cache.

    The cache is implemented as a SQLite database because it is serverless.

    Args:
        cache_dir: The path to where the cache was stored.
        key: The key to search for in the database.

    Returns:
        The integer value corresponding to the key in the database.
    """
    database_file: Path = cache_dir / "consumo.db"
    current_time: int | float = time.time()

    try:
        with sqlite3.connect(database_file) as connection:
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
