# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing images."""

import math

from pydantic import NonNegativeInt, validate_call


@validate_call
def calculate_viewing_time(image_count: NonNegativeInt) -> int:
    """Calculate the time for viewing images based on count.

    Args:
        image_count: The number of images.

    Returns:
        The time in seconds to view all the images.
    """
    first_ten_images_time: int = 75

    if image_count > 10:
        after_ten_images_time: int = (image_count - 10) * 3

        return first_ten_images_time + after_ten_images_time

    # For the first ten images, the time follows an arithmetic progression of:
    # S_{n} = \frac{n(25 - n)}{2}
    image_time: int | float = (image_count * (25 - image_count)) / 2

    return math.ceil(image_time)
