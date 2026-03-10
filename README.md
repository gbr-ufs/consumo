# consumo: Content Consumption Analyzer

[![PyPI Package](https://img.shields.io/pypi/v/consumo.svg)](https://pypi.python.org/pypi/consumo)
[![Codecov](https://codecov.io/gh/gbr-ufs/consumo/graph/badge.svg?token=IIRDADQH1Q)](https://codecov.io/gh/gbr-ufs/consumo)
[![Downloads](https://static.pepy.tech/badge/consumo/month)](https://pepy.tech/project/consumo)
[![License](https://img.shields.io/badge/license_-GPL-822422?logo=GNU&logoColor=black&labelColor=white)](LICENSE)

![GIF showcasing the program being used, by revealing it would take 21 minutes and 18 seconds to read the entire license at the standard 265 words per minute.](https://vhs.charm.sh/vhs-1mimEmoE9cISfgnplgT7xA.gif)

<p align="center">
  <a href="https://vhs.charm.sh">
    <img alt="VHS" src="https://stuff.charm.sh/vhs/badge.svg">
  </a>
</p>

## Introduction

`consumo` is a command-line interface (CLI) built with [Typer](https://typer.tiangolo.com/) that **calculates the time to consume either online or offline media**. It can be used for sorting media by duration for later consumption or by deciding if something can be viewed today or at a later date.

It's designed with **broad support** in mind. When it comes to online media, it supports video platforms by directly getting the duration of the linked video; online hosted files by extracting the duration from their metadata; articles and text in general by using the **Medium formula** to calculate the total consumption time based on text, using a (customizable) words per minute (WPM) count; image count; video duration of the videos on the page. For further details, see: [How Medium Calculates Read Time](https://mediumcourse.com/how-is-medium-article-read-time-calculated/).

For offline media, multiple backends are used to calculate the reading time. However, **by design**, local HTML files have **full feature parity** with online pages.

## CLI

Content Consumption Analyzer.

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: Print the program's version and exit.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `file`: Calculate the consumption time of files...
* `list`: Calculate the consumption time of all the links in a link list file...
* `url`: Calculate the consumption time of URLs...

### `file`

Calculate the consumption time of files concurrently in a *h *m *s format.

**Usage**:

```console
$ file [OPTIONS] FILES...
```

**Arguments**:

* `FILES...`: [required]

**Options**:

* `--sort / --no-sort`: Sort the output by duration in ascending order.  [default: no-sort]
* `--words-per-minute INTEGER`: Reading speed in words per minute.  [default: 265]
* `--help`: Show this message and exit.

### `list`

Calculate the consumption time of all the links in a link list file in a *h *m *s format.

Example:
    A "file with a list of links" is a plain text file that looks like this:

    ```text
    https://en.wikipedia.org/wiki/Python_(programming_language)
    https://en.wikipedia.org/wiki/High-level_programming_language
    https://en.wikipedia.org/wiki/General-purpose_programming_language
    https://en.wikipedia.org/wiki/Code_readability
    https://en.wikipedia.org/wiki/Significant_indentation
    https://en.wikipedia.org/wiki/Type_system#DYNAMIC
    https://en.wikipedia.org/wiki/Garbage_collection_(computer_science)
    https://en.wikipedia.org/wiki/Programming_paradigm
    https://en.wikipedia.org/wiki/Structured_programming
    https://en.wikipedia.org/wiki/Procedural_programming
    https://en.wikipedia.org/wiki/Object-oriented_programming
    https://en.wikipedia.org/wiki/Functional_programming
    ...
    ```

**Usage**:

```console
$ list [OPTIONS] FILE
```

**Arguments**:

* `FILE`: [required]

**Options**:

* `--sort / --no-sort`: Sort the output by duration in ascending order.  [default: no-sort]
* `--words-per-minute INTEGER`: Reading speed in words per minute.  [default: 265]
* `--help`: Show this message and exit.

### `url`

Calculate the consumption time of URLs concurrently in a *h *m *s format.

**Usage**:

```console
$ url [OPTIONS] URLS...
```

**Arguments**:

* `URLS...`: [required]

**Options**:

* `--sort / --no-sort`: Sort the output by duration in ascending order.  [default: no-sort]
* `--words-per-minute INTEGER`: Reading speed in words per minute.  [default: 265]
* `--help`: Show this message and exit.

### Configuration file

consumo supports a [TOML](https://toml.io/en/) under your system's default configuration directory (on Linux, `$XDG_CONFIG/HOME/config.toml`). It has these default values:

```toml
[general]
sort = false
words_per_minute = 265
```

## Context

I'm pretty unorganized. No matter how much I try to tidy things up, I always manage to make a mess somewhere else. In this case, I host in my own machine a [FreshRSS](https://github.com/FreshRSS/FreshRSS) container which should **ideally** be my only source of online content and things should be saved there. However, after hoarding 30+ tabs on my phone with random links from the web, I decided to make a file like this on my computer:

```text
https://en.wikipedia.org/wiki/Python_(programming_language)
https://en.wikipedia.org/wiki/High-level_programming_language
https://en.wikipedia.org/wiki/General-purpose_programming_language
https://en.wikipedia.org/wiki/Code_readability
https://en.wikipedia.org/wiki/Significant_indentation
https://en.wikipedia.org/wiki/Type_system#DYNAMIC
https://en.wikipedia.org/wiki/Garbage_collection_(computer_science)
https://en.wikipedia.org/wiki/Programming_paradigm
https://en.wikipedia.org/wiki/Structured_programming
https://en.wikipedia.org/wiki/Procedural_programming
https://en.wikipedia.org/wiki/Object-oriented_programming
https://en.wikipedia.org/wiki/Functional_programming
...
```

Repeat until you get over **a hundred** links (and multiple websites other than Wikipedia). Needless to say, I felt overwhelmed and thought: "LLMs can view webpages. Maybe I can give this list of links to one so it can sort them by duration for a better experience?"

I tried multiple models, but none where able to do that. Maybe there's something like this out there already, but I forgot to search for it. But thankfully that sparkled a great idea for a project: consumo!

## Philosophies

- Dependency Injection.
- Parse, don't validate[^1].
- Test Driven Development[^2].

[^1]: King, A. (2019) Parse, don’t validate. Alexis King’s Blog. Available at: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/ (Accessed: September 29, 2025).

[^2]: Beck, K. (2003) Test-driven development: By example. Boston: Addison-Wesley (The Addison-Wesley signature series).
