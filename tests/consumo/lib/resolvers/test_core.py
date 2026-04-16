# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suit of the lib/resolvers/core module."""

from consumo.lib.resolvers.core import dummy_cache_resolver, dummy_get_cached_resolver


def test_dummy_cache_resolver() -> None:
    assert dummy_cache_resolver("consumo", "foo.txt", 1, 1) is None


def test_dummy_get_cached_resolver() -> None:
    assert dummy_get_cached_resolver("consumo", "foo.txt", 1) is None
