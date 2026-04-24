# Environment Variables

consumo supports environment variables for configuration. The order of priority goes like this: configuration file -> CLI flags -> environment variables -> program defaults.

## General

### `CONSUMO_SORT`

Equivalent to the `--sort` flag of [the commands](references/cli.md). Determines whether the output will be sorted by duration in ascending order.

### `CONSUMO_WPM`

Equivalent to the `--words-per-minute` flag of [the commands](references/cli.md). Determines the reading speed in words per minute.

### `CONSUMO_SKIP_ERRORS`

Equivalent to the `--skip-errors` flag of [the commands](references/cli.md). Determines whether to show zero seconds for arguments that otherwise would make the program exit with an error.

### `CONSUMO_CONFIG_FILE`

Sets the configuration file of the program.

## URL

### `CONSUMO_CACHE`

Equivalent to the `--cache` flag of [the url command](references/cli.md#consumo-url). Determines whether to cache results in a database for later reuse.

### `CONSUMO_DEPTH`

Equivalent to the `--depth` flag of [the url command](references/cli.md#consumo-url). Determines how many levels to recursively follow URLs on the page. It is recommended that one pairs it with `skip_errors` at high levels, as the availability of unvisited URLs is unknown (as in, you can't know if you can follow a URL if you haven't clicked it).

### `CONSUMO_CACHE_DIR`

Equivalent to the `--cache-dir` flag of [the url command](references/cli.md#consumo-url). Determines the path to where the cache will be stored.
