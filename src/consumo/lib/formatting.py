# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for formatting data."""


def format_time(total_seconds: int) -> str:
    """Format the duration/consumption time given in seconds in a *h *m *s format.

    Args:
        total_seconds: The duration/consumption time in seconds of the content.

    Returns:
        The duration/consumption time in a *h *m *s format.
    """
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    hours %= 24

    parts: list[str] = []

    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")

    parts.append(f"{seconds}s")

    return " ".join(parts)
