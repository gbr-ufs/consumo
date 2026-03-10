# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the lib/file/image module."""

import pytest

from consumo.lib.file.image import calculate_viewing_time


@pytest.mark.parametrize(
    "image_count, expected_image_time", [(10, 75), (11, 78), (0, 0)]
)
def test_calculate_viewing_time(image_count: int, expected_image_time: int) -> None:
    actual_image_time: int = calculate_viewing_time(image_count)

    assert actual_image_time == expected_image_time
