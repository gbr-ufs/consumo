# SPDX-License-Identifier: GPL-3.0-or-later

"""Test suite of the cli/url module."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

from av.error import FFmpegError
from pydantic import HttpUrl
from typer.testing import CliRunner, Result

from consumo.cli.url import app
from tests import FIXTURES_DIR

runner: CliRunner = CliRunner()


@patch("consumo.lib.handlers.url.urllib.request.urlopen")
@patch("consumo.lib.url.trafilatura.fetch_url")
@patch("consumo.lib.handlers.url.get_hosted_multimedia_duration")
@patch("consumo.lib.url.get_absolute_path_multimedia_duration")
@patch("consumo.lib.handlers.url.get_multimedia_duration")
def test_app(
    mock_get_multimedia_duration: Mock,
    mock_get_absolute_path_multimedia_duration: Mock,
    mock_get_hosted_multimedia_duration: Mock,
    mock_trafilatura_fetch_url: Mock,
    mock_urllib_request_urlopen: Mock,
) -> None:
    url_html: Path = FIXTURES_DIR / "url.html"

    def mock_get_multimedia_duration_side_effect(url: HttpUrl) -> int:
        if url == HttpUrl(
            "https://dn710704.ca.archive.org/0/items/night_of_the_living_dead_dvd/Night.mp4"
        ):
            return 5732

        raise FFmpegError(0, "", "")

    def mock_get_absolute_path_multimedia_duration_side_effect(url: HttpUrl) -> int:
        if url == HttpUrl("https://www.youtube.com/watch?v=l-FGlw6jWgQ"):
            return 5713

        return 1

    def mock_trafilatura_fetch_url_side_effect(url: str) -> str:
        url_str: dict[str, str] = {
            "https://gbr-ufs.github.io/consumo/url": url_html.read_text("utf-8"),
            "https://info.cern.ch/hypertext/WWW/TheProject.html": r"""<HEADER>\n<TITLE>The World Wide Web project</TITLE>\n<NEXTID N="55">\n</HEADER>\n<BODY>\n<H1>World Wide Web</H1>The WorldWideWeb (W3) is a wide-area<A\nNAME=0 HREF="WhatIs.html">\nhypermedia</A> information retrieval\ninitiative aiming to give universal\naccess to a large universe of documents.<P>\nEverything there is online about\nW3 is linked directly or indirectly\nto this document, including an <A\nNAME=24 HREF="Summary.html">executive\nsummary</A> of the project, <A\nNAME=29 HREF="Administration/Mailing/Overview.html">Mailing lists</A>\n, <A\nNAME=30 HREF="Policy.html">Policy</A> , November\'s  <A\nNAME=34 HREF="News/9211.html">W3  news</A> ,\n<A\nNAME=41 HREF="FAQ/List.html">Frequently Asked Questions</A> .\n<DL>\n<DT><A\nNAME=44 HREF="../DataSources/Top.html">What\'s out there?</A>\n<DD> Pointers to the\nworld\'s online information,<A\nNAME=45 HREF="../DataSources/bySubject/Overview.html"> subjects</A>\n, <A\nNAME=z54 HREF="../DataSources/WWW/Servers.html">W3 servers</A>, etc.\n<DT><A\nNAME=46 HREF="Help.html">Help</A>\n<DD> on the browser you are using\n<DT><A\nNAME=13 HREF="Status.html">Software Products</A>\n<DD> A list of W3 project\ncomponents and their current state.\n(e.g. <A\nNAME=27 HREF="LineMode/Browser.html">Line Mode</A> ,X11 <A\nNAME=35 HREF="Status.html#35">Viola</A> ,  <A\nNAME=26 HREF="NeXT/WorldWideWeb.html">NeXTStep</A>\n, <A\nNAME=25 HREF="Daemon/Overview.html">Servers</A> , <A\nNAME=51 HREF="Tools/Overview.html">Tools</A> ,<A\nNAME=53 HREF="MailRobot/Overview.html"> Mail robot</A> ,<A\nNAME=52 HREF="Status.html#57">\nLibrary</A> )\n<DT><A\nNAME=47 HREF="Technical.html">Technical</A>\n<DD> Details of protocols, formats,\nprogram internals etc\n<DT><A\nNAME=40 HREF="Bibliography.html">Bibliography</A>\n<DD> Paper documentation\non  W3 and references.\n<DT><A\nNAME=14 HREF="People.html">People</A>\n<DD> A list of some people involved\nin the project.\n<DT><A\nNAME=15 HREF="History.html">History</A>\n<DD> A summary of the history\nof the project.\n<DT><A\nNAME=37 HREF="Helping.html">How can I help</A> ?\n<DD> If you would like\nto support the web..\n<DT><A\nNAME=48 HREF="../README.html">Getting code</A>\n<DD> Getting the code by<A\nNAME=49 HREF="LineMode/Defaults/Distribution.html">\nanonymous FTP</A> , etc.</A>\n</DL>\n</BODY>\n""",
        }

        return url_str.get(url, "")

    def mock_urllib_request_urlopen_side_effect(url: str) -> Mock:
        mock_response: MagicMock = MagicMock()

        if url == "https://gbr-ufs.github.io/consumo/url":
            mock_response.read.return_value = url_html.read_text("utf-8")
        else:
            mock_response.read.return_value = b""

        mock_response.__enter__.return_value = mock_response

        return mock_response

    mock_get_multimedia_duration.side_effect = mock_get_multimedia_duration_side_effect
    mock_get_absolute_path_multimedia_duration.side_effect = (
        mock_get_absolute_path_multimedia_duration_side_effect
    )
    mock_get_hosted_multimedia_duration.return_value = 5713
    mock_trafilatura_fetch_url.side_effect = mock_trafilatura_fetch_url_side_effect
    mock_urllib_request_urlopen.side_effect = mock_urllib_request_urlopen_side_effect

    actual_result: Result = runner.invoke(
        app,
        [
            "https://dn710704.ca.archive.org/0/items/night_of_the_living_dead_dvd/Night.mp4",
            "https://www.youtube.com/watch?v=l-FGlw6jWgQ",
            "https://gbr-ufs.github.io/consumo/url",
            "LICENSE",
            "--depth",
            "1",
            "--skip-errors",
            "--sort",
        ],
    )
    expected_exit_code: int = 0
    expected_error: str = "ValidationError"
    # Line breaks on Windows are "\r\n" instead of "\n", which ends up breaking
    # count.
    url_html_expected_result: str = (
        "1h 37m 49s" if sys.platform == "win32" else "1h 37m 46s"
    )
    expected_results: list[str] = [
        "0s",
        "1h 35m 13s",
        "1h 35m 32s",
        url_html_expected_result,
    ]

    assert actual_result.exit_code == expected_exit_code
    assert expected_error in actual_result.output
    for expected_result in expected_results:
        assert expected_result in actual_result.output
