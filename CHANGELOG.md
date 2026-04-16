## 0.12.1 (2026-04-16)

### Fix

- make cache functions error out instead of returning none

## 0.12.0 (2026-04-16)

### Feat

- make get_duration functions public
- implement dependency injection for caching

## 0.11.1 (2026-04-09)

### Refactor

- unhard code beautiful soup parser

### Perf

- cut down on url time

## 0.11.0 (2026-04-09)

### Feat

- **file.py**: add caching for multimedia files

### Fix

- **cache.py**: create parent directories for cache

## 0.10.0 (2026-04-09)

### Feat

- **config.py**: implement environment variable-based configuration

### Fix

- error handling
- **cli/url.py**: use courlan.clean_url instead of courlan.check_url

## 0.9.0 (2026-03-30)

### Feat

- implement --cache flag
- **list.py**: support --depth for list command

## 0.8.0 (2026-03-28)

### Feat

- implement --depth flag

## 0.7.0 (2026-03-28)

### Feat

- implement --skip-errors flag

## 0.6.1 (2026-03-27)

### Fix

- calculate_reading_time cjk implementation

## 0.6.0 (2026-03-27)

### BREAKING CHANGE

- modify return type of get_word_count from int to tuple[int, int]

### Feat

- implement caching for the url command
- implement caching for the file command

### Refactor

- (attempt to?) improve precision for text with cjk

### Perf

- add caching module

## 0.5.0 (2026-03-22)

### BREAKING CHANGE

- remove `get_image_count`
- modify the value of cjk characters, changing the result for content with these characters

### Fix

- modify cjk character value to be about half a word

### Refactor

- calculate_html_consumption_time

### Perf

- **text.py**: use findall method instead of a loop

## 0.4.2 (2026-03-20)

### Fix

- **pyproject.toml**: update uv build

### Refactor

- use import instead of import-from for trafilatura functions

## 0.4.1 (2026-03-18)

### Fix

- **config.tap**: minor fix to tag another version

## 0.4.0 (2026-03-18)

### Feat

- **text**: add preliminary cjk support
- **multimedia.py**: implement concurrency
- **multimedia.py**: add playlist support
- further generalize deprecated video module to support more file types

### Fix

- run "uv run zensical" instead of running "zensical" directly
- **cli/url.py**: use baseline ffmpeg error

### Refactor

- **html.py**: use sum instead of unecessary loop

## 0.3.0 (2026-03-10)

### Feat

- **__init__.py**: expose public api

## 0.2.0 (2026-03-10)

### BREAKING CHANGE

- this removes the version subcommand.

### Feat

- add configuration file support
- **main.py**: show help when no arguments are given

### Fix

- type annotations
- **.pre-commit-config.yaml**: commitizen hook stage

### Refactor

- move video code into multimedia module
- drop version subcommand in favour of a dynamic version option
- drop state approach in favour of a more functional one
- move format_time out of the core module
- **core.py**: move out of lib directory
- **html.py**: use map instead of future
- **core.py**: use divmod instead of sequential division and module operations
- **cli/file.py**: remove unecessary try/catch block
- **state.py**: move state out of lib

### Perf

- **dev**: replace pre-commit with prek

## 0.1.1 (2026-03-08)

### Fix

- small commit to bump version

## 0.1.0 (2026-03-08)

### Feat

- init
