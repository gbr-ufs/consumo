# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suit of the lib/resolvers/core module."""

import pytest

from consumo.lib.exceptions import NoCacheError
from consumo.lib.resolvers.core import dummy_cache_resolver, dummy_get_cached_resolver


def test_dummy_cache_resolver() -> None:
    assert dummy_cache_resolver("consumo", "https://example.com", 1, 1) is None


def test_dummy_get_cached_resolver() -> None:
    with pytest.raises(NoCacheError):
        dummy_get_cached_resolver("consumo", "https://example.com") is None
