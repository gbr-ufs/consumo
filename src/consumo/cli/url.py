# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

import typer
from av.error import InvalidDataError
from pydantic import HttpUrl, PositiveInt, validate_call
from typer import Typer
from yt_dlp.utils import DownloadError

from consumo.lib.cli.core import (
    execute_concurrent_command,
)
from consumo.lib.cli.state import configuration
from consumo.lib.exceptions import MissingMetadataError
from consumo.lib.file.multimedia import get_duration as get_multimedia_duration
from consumo.lib.file.video import get_video_platform_video_duration
from consumo.lib.types import Second
from consumo.lib.url import calculate_consumption_time

app: Typer = Typer()


@validate_call
def get_duration(url: HttpUrl, words_per_minute: PositiveInt) -> Second:
    try:
        return get_video_platform_video_duration(url)
    except DownloadError:
        pass
    except MissingMetadataError:
        pass

    try:
        return get_multimedia_duration(url)
    except InvalidDataError:
        pass

    return calculate_consumption_time(url, words_per_minute)


@app.command("url")
def process_url(
    urls: Annotated[list[str], typer.Argument(exists=True, readable=True)],
) -> None:
    def duration_resolver(url: str) -> Second:
        return get_duration(HttpUrl(url), configuration.words_per_minute)

    execute_concurrent_command(
        urls,
        duration_resolver,
        "Processing URLs...",
    )
