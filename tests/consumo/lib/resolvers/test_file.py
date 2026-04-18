# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/resolvers/file module."""

from pathlib import Path

import pytest

from consumo.lib.exceptions import UnsupportedMIMETypeError
from consumo.lib.resolvers.file import get_duration


def test_get_duration_unsupported_mime_type_error(tmp_path: Path) -> None:
    mock_executable: Path = tmp_path / "executable"

    # Standard magic bytes for a Unix executable.
    mock_executable.write_bytes(
        b"\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )

    with pytest.raises(UnsupportedMIMETypeError):
        get_duration(mock_executable)
