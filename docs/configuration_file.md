# Configuration File

consumo supports a [TOML](https://toml.io/en/) configuration file under your system's default configuration directory (on Linux, `$XDG_CONFIG_HOME/consumo/config.toml`). It has these default values:

```toml
[general]
sort = false
words_per_minute = 265
skip_errors = false
```

## `general`

### `sort`

Equivalent to the `--sort` flag of [the commands](cli.md). Determines whether the output will be sorted by duration in ascending order.

### `words_per_minute`

Equivalent to the `--words-per-minute` flag of [the commands](cli.md). Determines the reading speed in words per minute.

### `skip_errors`

Equivalent to the `--skip-errors` flag of [the commands](cli.md). Determines whether to show zero seconds for arguments that otherwise would make the program exit with an error.
