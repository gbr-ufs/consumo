# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/classes module."""

from consumo.lib.classes import SilentLogger


def test_silent_logger() -> None:
    logger: SilentLogger = SilentLogger()

    assert logger.debug("test debug") is None
    assert logger.warning("test warning") is None
    assert logger.error("test error") is None
