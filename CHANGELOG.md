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
