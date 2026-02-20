# SPDX-License-Identifier: GPL-3.0-or-later

import math

from pydantic import NonNegativeInt, validate_call

from consumo.lib.types import DecimalSecond, Second


@validate_call
def calculate_viewing_time(image_count: NonNegativeInt) -> Second:
    first_ten_images_time: Second = 75

    if image_count > 10:
        after_ten_images_time: Second = (image_count - 10) * 3

        return first_ten_images_time + after_ten_images_time

    # For the first ten images, the time follows an arithmetic progression of:
    # S_{n} = \frac{n(25 - n)}{2}
    image_time: Second | DecimalSecond = (image_count * (25 - image_count)) / 2

    return math.ceil(image_time)
