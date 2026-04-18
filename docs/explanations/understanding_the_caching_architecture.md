# Understanding the Caching Architecture

consumo supports caching for URLs, as that path takes longer than the file one. For a better library experience, consumo uses [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection) to provide a database-agnostic caching experience.

## The Core Logic is Database-Agnostic

The URL version of the `get_duration` function, `get_url_duration` relies on two function parameters for caching needs:

`get_cached_resolver(program_name: str, key: str) -> int`

:   Gets the value assigned to `key` from the cache.

`cache_resolver(program_name: str, value: int, time_to_live: int) -> int`

:   Saves the value related to `key` in the cache.

These parameters are dummy by default so one has to implement them with the caching backend they have in mind before considering the use of caching.

## How the CLI Uses It

consumo has a built-in [SQLite](https://sqlite.org/) implementation. SQLite was picked because it is a serverless database. That means you don't need to have a massive database server running in the background just to use a CLI.

## Why Build It This Way?

This allows developers to scale up consumo's implementation of consumption time calculation, in case they want to integrate it into a larger program, that may need a larger database.
