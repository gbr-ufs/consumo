# SPDX-License-Identifier: GPL-3.0-or-later

"""Content Consumption Analyzer."""

from consumo.lib.exceptions import ConsumoError, MissingMetadataError
from consumo.lib.file.html import (
    calculate_consumption_time as calculate_html_consumption_time,
)
from consumo.lib.file.html import (
    extract_text as extract_html_text,
)
from consumo.lib.file.html import (
    extract_videos,
    get_custom_player_duration,
    get_image_count,
)
from consumo.lib.file.html import (
    get_relative_path_video_duration as get_html_relative_path_video_duration,
)
from consumo.lib.file.html import (
    get_video_duration as get_html_video_duration,
)
from consumo.lib.file.image import calculate_viewing_time
from consumo.lib.file.mass_media import (
    calculate_consumption_time as calculate_mass_media_consumption_time,
)
from consumo.lib.file.mass_media import extract_text as extract_mass_media_text
from consumo.lib.file.multimedia import get_duration as get_multimedia_duration
from consumo.lib.file.text import calculate_reading_time, get_word_count
from consumo.lib.file.text import (
    calculate_consumption_time as calculate_text_consumption_time,
)
from consumo.lib.formatting import format_time
from consumo.lib.url import (
    calculate_consumption_time as calculate_url_consumption_time,
)
from consumo.lib.url import (
    get_relative_path_video_duration as get_url_relative_path_video_duration,
)
from consumo.lib.url import (
    get_video_duration as get_url_video_duration,
)

__all__: list[str] = [
    "calculate_html_consumption_time",
    "extract_html_text",
    "extract_videos",
    "get_custom_player_duration",
    "get_image_count",
    "get_html_relative_path_video_duration",
    "get_html_video_duration",
    "calculate_viewing_time",
    "calculate_mass_media_consumption_time",
    "extract_mass_media_text",
    "get_multimedia_duration",
    "get_word_count",
    "calculate_reading_time",
    "calculate_text_consumption_time",
    "format_time",
    "calculate_url_consumption_time",
    "get_url_relative_path_video_duration",
    "get_url_video_duration",
]
