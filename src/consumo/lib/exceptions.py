# SPDX-License-Identifier: GPL-3.0-or-later

"""Custom exception classes for the program."""


class ConsumoError(Exception):
    """Base class for consumo exceptions."""


class MissingMetadataError(ConsumoError):
    """Raised when a backend can't get the duration of a file from its metadata."""


class UnsupportedMIMETypeError(ConsumoError):
    """Raised when a file doesn't have the expected MIME type."""
