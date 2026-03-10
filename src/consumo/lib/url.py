# SPDX-License-Identifier: GPL-3.0-or-later

"""URL duration extract and consumption time logic."""

from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urljoin

from pydantic import (
    HttpUrl,
    NonNegativeInt,
    ValidationError,
    validate_call,
)
from trafilatura import fetch_url

from consumo.lib.file.html import (
    calculate_consumption_time as calculate_html_consumption_time,
)
from consumo.lib.file.video import get_duration as get_absolute_path_video_duration


@validate_call
def get_relative_path_video_duration(url: HttpUrl, video: Path) -> int:
    """Resolve a URL to get the duration of a video with a relative path.

    Args:
        url: URL where the video was originally found.
        video: Relative path used for the video's "src" attribute.

    Returns:
        The duration of the video in seconds.
    """
    resolved: str = urljoin(str(url), str(video))

    return get_absolute_path_video_duration(HttpUrl(resolved))


@validate_call
def get_video_duration(url: HttpUrl, video: str) -> int:
    """Get the duration of a video hosted online.

    Tries to treat the video as if it had an absolute path, then tries to
    resolve its path if that fails.

    Args:
        url: URL where the video was originally found for path resolution.
        video: Path used for the video's "src" attribute.

    Returns:
        The duration of the video in seconds.
    """
    try:
        return get_absolute_path_video_duration(HttpUrl(video))
    except ValidationError:
        # If HttpUrl(video) fails validation, the "src" is likely a relative
        # path rather than a URL.
        return get_relative_path_video_duration(url, Path(video))


@validate_call
def calculate_consumption_time(
    url: HttpUrl, words_per_minute: NonNegativeInt = 265
) -> int:
    """Calculate the consumption time of a URL in seconds.

    Avoids code duplication by downloading the HTML of the URL to a temporary
    file, to use the HTML backend `calculate_html_consumption_time`.

    Args:
        url: URL pointing to the content whose consumption time will be analyzed.
        words_per_minute: Reading speed in words per minute.

    Returns:
        The time in seconds to consume the content the URL points to.

    Raises:
        ConnectionError: If the HTML content of the URL wasn't downloaded.
    """
    html_content: str | None = fetch_url(str(url))

    if html_content is None:
        raise ConnectionError

    with TemporaryDirectory() as tmp_dir:
        html: Path = Path(tmp_dir) / "temp.html"

        html.write_text(html_content, "utf-8")

        return calculate_html_consumption_time(
            html, words_per_minute, lambda video: get_video_duration(url, video)
        )
