# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/url module."""

from unittest.mock import Mock, patch

import pytest
from pydantic import HttpUrl

from consumo.lib.url import (
    calculate_consumption_time,
)


@patch("consumo.lib.url.trafilatura.fetch_url")
def test_calculate_consumption_time_connectionerror(
    mock_trafilatura_fetch_url: Mock,
) -> None:
    url: HttpUrl = HttpUrl("https://example.com/url")
    mock_trafilatura_fetch_url.return_value = None

    with pytest.raises(ConnectionError):
        calculate_consumption_time(url)
