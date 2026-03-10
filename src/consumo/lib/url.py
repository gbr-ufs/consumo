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
from consumo.lib.file.multimedia import (
    get_hosted_multimedia_duration as get_absolute_path_multimedia_duration,
)


@validate_call
def get_relative_path_multimedia_duration(url: HttpUrl, src: Path) -> int:
    """Resolve a URL to get the duration of a multimedia file with a relative path.

    Args:
        url: URL where the multimedia file was originally found.
        src: Relative path used for the multimedia file's "src" attribute.

    Returns:
        The duration of the content in seconds.
    """
    resolved: str = urljoin(str(url), str(src))

    return get_absolute_path_multimedia_duration(HttpUrl(resolved))


@validate_call
def get_multimedia_duration(url: HttpUrl, src: str) -> int:
    """Get the duration of a multimedia hosted online.

    Tries to treat the file as if it had an absolute path, then tries to
    resolve its path if that fails.

    Args:
        url: URL where the multimedia file was originally found for
            path resolution.
        src: Path used for the multimedia file's "src" attribute.

    Returns:
        The duration of the content in seconds.
    """
    try:
        return get_absolute_path_multimedia_duration(HttpUrl(src))
    except ValidationError:
        # If HttpUrl(src) fails validation, then src is likely a relative
        # path rather than a URL.
        return get_relative_path_multimedia_duration(url, Path(src))


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
            html, words_per_minute, lambda src: get_multimedia_duration(url, src)
        )
