# SPDX-License-Identifier: GPL-3.0-or-later

"""Global CLI state definition module."""

from dataclasses import dataclass

from pydantic import PositiveInt


@dataclass
class GlobalConfiguration:
    """Class containing the settings available to all consumo commands.

    Attributes:
        sort: Whether to sort the output in ascending order before printing.
        words_per_minute: Reading speed in words per minute.
    """

    sort: bool = False
    words_per_minute: PositiveInt = 265


configuration = GlobalConfiguration()
