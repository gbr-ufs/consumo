# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Module containing classes for abstraction."""


class SilentLogger:
    """Class for silencing programs that use a custom object for logging."""

    def debug(self, msg: str) -> None:
        """Discard debug messages.

        Args:
            msg: Debug message to be discarded.
        """

    def warning(self, msg: str) -> None:
        """Discard warning messages.

        Args:
            msg: Warning message to be discarded.
        """

    def error(self, msg: str) -> None:
        """Discard error messages.

        Args:
            msg: Error message to be discarded.
        """
