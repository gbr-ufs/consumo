# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from pydantic import PositiveInt


@dataclass
class GlobalConfiguration:
    sort: bool = False
    words_per_minute: PositiveInt = 265


configuration = GlobalConfiguration()
