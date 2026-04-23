# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Content Consumption Analyzer."""

from consumo.lib.exceptions import (
    ConsumoError,
    MissingMetadataError,
    NoCacheError,
    UnsupportedMIMETypeError,
)
from consumo.lib.file.html import (
    calculate_consumption_time as calculate_html_consumption_time,
)
from consumo.lib.file.html import (
    extract_multimedias,
    get_custom_player_duration,
)
from consumo.lib.file.html import (
    get_multimedia_duration as get_html_multimedia_duration,
)
from consumo.lib.file.image import calculate_viewing_time
from consumo.lib.file.mass_media import (
    calculate_consumption_time as calculate_mass_media_consumption_time,
)
from consumo.lib.file.mass_media import extract_text as extract_mass_media_text
from consumo.lib.file.multimedia import (
    get_duration as get_url_multimedia_duration,
)
from consumo.lib.file.multimedia import (
    get_multimedia_duration,
)
from consumo.lib.file.text import (
    calculate_consumption_time as calculate_text_consumption_time,
)
from consumo.lib.file.text import calculate_reading_time, get_word_count
from consumo.lib.formatting import format_time
from consumo.lib.handlers.file import get_duration as get_file_duration
from consumo.lib.handlers.url import get_duration as get_url_duration
from consumo.lib.url import (
    calculate_consumption_time as calculate_url_consumption_time,
)

__all__: list[str] = [
    "ConsumoError",
    "MissingMetadataError",
    "calculate_html_consumption_time",
    "calculate_mass_media_consumption_time",
    "calculate_reading_time",
    "calculate_text_consumption_time",
    "calculate_url_consumption_time",
    "calculate_viewing_time",
    "extract_mass_media_text",
    "extract_multimedias",
    "format_time",
    "get_custom_player_duration",
    "get_file_duration",
    "get_html_multimedia_duration",
    "get_multimedia_duration",
    "get_url_duration",
    "get_url_multimedia_duration",
    "get_word_count",
    "MissingMetadataError",
    "NoCacheError",
    "UnsupportedMIMETypeError",
]
