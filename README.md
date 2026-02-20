# consumo

***Content consumption analyzer CLI***

# Summary

`consumo` is a CLI built with [Typer](https://typer.tiangolo.com/) that calculates the time to consume some form of content using the [Medium formula](https://mediumcourse.com/how-is-medium-article-read-time-calculated/).

# Supported Arguments

`consumo` is meant to primarily be used with a text file full of URLs, through the `list` subcommand. Basically, files that look like this:

```text
https://github.com/gbr-ufs/pf
https://github.com/gbr-ufs/cses
https://github.com/gbr-ufs/notes
https://github.com/gbr-ufs/ies
https://github.com/gbr-ufs/hack-ia-mockup
https://github.com/gbr-ufs/probabilidade-detran-se
https://github.com/gbr-ufs/hello-r-markdown
```

## File Types

- [audio](https://www.iana.org/assignments/media-types/media-types.xhtml#audio).
- [text](https://www.iana.org/assignments/media-types/media-types.xhtml#text).

## URLs

`consumo` supports any kind of URL. [YouTube](https://www.youtube.com/) links are treated differently: passing a YouTube link to `consumo` returns its length.

# Usage

```sh
consumo file FILE --output FILE --sort
```

```sh
consumo list FILE --output FILE --sort
```

```sh
consumo url TEXT --output FILE --sort
```

# Skills

By developing this project, I demonstrate that I know:

- [Git](https://git-scm.com).
- [GitHub](https://github.com).
- [Markdown](https://daringfireball.net/projects/markdown).
- [Python](https://www.python.org/).

## Python

- [av](https://pyav.org/docs/stable/).
- [bs4](https://beautiful-soup-4.readthedocs.io/en/latest/).
- [lxml](https://lxml.de/).
- [pre-commit](https://pre-commit.com/).
- [pydantic](https://docs.pydantic.dev/latest/).
- [pyinstaller](https://pyinstaller.org/en/stable/).
- [pymupdf](https://pymupdf.io/).
- [pytest](https://docs.pytest.org/en/stable/).
- [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/index.html).
- [python-magic](https://pypi.org/project/python-magic/).
- [rich](https://rich.readthedocs.io/en/stable/introduction.html).
- [ruff](https://docs.astral.sh/ruff/).
- [trafilatura](https://trafilatura.readthedocs.io/en/latest/index.html).
  - [brotli](https://github.com/google/brotli).
  - [faust-cchardet](https://github.com/PyYoshi/cChardet).
  - [python-zstandard](https://github.com/indygreg/python-zstandard).
- [ty](https://docs.astral.sh/ty/).
- [typer](https://typer.tiangolo.com/).
- [uv](https://docs.astral.sh/uv/).
- [yt-dlp](https://github.com/yt-dlp/yt-dlp).
- [zensical](https://zensical.org/).

## Additional Skills

- [commitizen](https://commitizen-tools.github.io/commitizen/).
- [Development Containers](https://containers.dev/).
- [direnv](https://direnv.net/).
- [EditorConfig](https://editorconfig.org/).
- [GitHub Actions](https://docs.github.com/en/actions).
- [MIME Types](https://www.iana.org/assignments/media-types/media-types.xhtml).
- [Nix](https://nixos.org/).

## Philosophies

- Dependency Injection.[^1]
- [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/).
- Test Driven Development.[^1]

[^1]: Used for the HTML variant of `calculate_consumption_time` so the URL variant can reuse it. This is done in the `video_duration_resolver` parameter.
[^2]: Beck, K. (2003) Test-driven development: By example. Boston: Addison-Wesley (The Addison-Wesley signature series).
