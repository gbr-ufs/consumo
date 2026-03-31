# Configuration File

consumo supports a [TOML](https://toml.io/en/) configuration file under your system's default configuration directory (on Linux, `$XDG_CONFIG_HOME/consumo/config.toml`). It has these default values:

```toml
[general]
sort = false
words_per_minute = 265
skip_errors = false
cache = true

[url]
depth = 0
```

## `general`

### `sort`

Equivalent to the `--sort` flag of [the commands](cli.md). Determines whether the output will be sorted by duration in ascending order.

### `words_per_minute`

Equivalent to the `--words-per-minute` flag of [the commands](cli.md). Determines the reading speed in words per minute.

### `skip_errors`

Equivalent to the `--skip-errors` flag of [the commands](cli.md). Determines whether to show zero seconds for arguments that otherwise would make the program exit with an error.

### `cache`

Equivalent to the `--cache` flag of [the commands](cli.md). Determines whether to cache results in a database for later reuse.

## `url`

### `depth`

Equivalent to the `--depth` flag of [the url command](cli.md). Determines how many levels to recursively follow URLs on the page. It is recommended that one pairs it with `skip_errors` at high levels, as the availability of unvisited URLs is unknown (as in, you can't know if you can follow a URL if you haven't clicked it).
