# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suit of the lib/handlers/core module."""

from pathlib import Path

import pytest

from consumo.lib.exceptions import NoCacheError
from consumo.lib.handlers.core import dummy_cache_resolver, dummy_get_cached_resolver


def test_dummy_cache_resolver() -> None:
    assert dummy_cache_resolver(Path("consumo"), "https://example.com", 1, 1) is None


def test_dummy_get_cached_resolver() -> None:
    with pytest.raises(NoCacheError):
        dummy_get_cached_resolver(Path("consumo"), "https://example.com") is None
