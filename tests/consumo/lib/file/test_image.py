# SPDX-License-Identifier: GPL-3.0-or-later

from pytest import mark

from consumo.lib.file.image import calculate_viewing_time
from consumo.lib.types import Second


@mark.parametrize("image_count, expected_image_time", [(10, 75), (11, 78), (0, 0)])
def test_calculate_viewing_time(image_count: int, expected_image_time: Second) -> None:
    actual_image_time: Second = calculate_viewing_time(image_count)

    assert actual_image_time == expected_image_time
