# YAML formatter for pre-commit git hooks

[![default](https://github.com/ITProKyle/pre-commit-hook-yamlfmt/actions/workflows/on-push.yml/badge.svg)](https://github.com/ITProKyle/pre-commit-hook-yamlfmt/actions/workflows/on-push.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![GitHub Release](https://img.shields.io/github/v/release/ITProKyle/pre-commit-hook-yamlfmt)](https://github.com/ITProKyle/pre-commit-hook-yamlfmt/releases)
[![renovate](https://img.shields.io/badge/enabled-brightgreen?logo=renovatebot&logoColor=%2373afae&label=renovate)](https://developer.mend.io/)

> [!NOTE]
> This project is a fork of [jumanjihouse/pre-commit-hook-yamlfmt](https://github.com/jumanjihouse/pre-commit-hook-yamlfmt).

YAML formatter for [`pre-commit`](http://pre-commit.com).

This hook formats the indentation of YAML files and optionally aligns top-level colons.
[`ruamel.yaml`](https://yaml.readthedocs.io/en/latest/) is used to roundtrip YAML files, preserving comments as much as possible.

> [!IMPORTANT]
> Each versioned release of this hook is pinned to an exact version of it's direct dependencies to limit unexpected changes.

## Options

| Option                                       | Default                  | Description                                         |
| -------------------------------------------- | ------------------------ | --------------------------------------------------- |
| `--allow-duplicate-keys/--no-duplicate-keys` | `--allow-duplicate-keys` | whether to allow duplicate keys                     |
| `--colons/--no-colons`                       | `--no-colons`            | whether to align top-level colons                   |
| `--implicit-start/--no-implicit-start`       | `implicit-start`         | whether to remove the explicit document start       |
| `--mapping, -m`                              | `4`                      | number of spaces to indent mappings (dictionaries)  |
| `--offset, -o`                               | `4`                      | number of spaces to offset the dash from sequences  |
| `--preserve-quotes/--no-preserve-quotes`     | `--preserve-quotes`      | whether to keep existing string quoting             |
| `--sequence, -s`                             | `6`                      | number of spaces to indent sequences (arrays/lists) |
| `--width, -w`                                | `4096`                   | maximum line width                                  |

## How-to

### Configure pre-commit

#### Use defaults

Add to `.pre-commit-config.yaml` in your git repo:

```yaml
- repo: https://github.com/ITProKyle/pre-commit-hook-yamlfmt
  rev: v0.2.1  # or specific tag
  hooks:
    - id: yamlfmt
```

> [!TIP]
> If a pre-commit hook changes a file, the hook fails with a warning that files were changed.

Given this input:

```yaml
foo:
  bar:
    - baz1
    - baz2
```

The default settings result in this output:

```yaml
---
foo:
  bar:
    - baz1
    - baz2
```

#### Combine with `yamllint`

`yamlfmt` only works with valid YAML files, so I recommend to use `yamllint` and `yamlfmt` together.

```yaml
- repo: https://github.com/adrienverge/yamllint.git
  rev: v1.21.0  # or higher tag
  hooks:
    - id: yamllint
      args: [--format, parsable, --strict]

- repo: https://github.com/ITProKyle/pre-commit-hook-yamlfmt
  rev: v0.2.1  # or specific tag
  hooks:
    - id: yamlfmt
```

#### Override defaults

Add to `.pre-commit-config.yaml` in your git repo:

```yaml
- repo: https://github.com/ITProKyle/pre-commit-hook-yamlfmt
  rev: v0.2.1  # or specific tag
  hooks:
    - id: yamlfmt
      args: [--mapping, '2', --sequence, '2', --offset, '0', --colons, --width, '150']
```

### Invoke pre-commit

#### On every commit

If you want to invoke the checks as a git pre-commit hook, run:

```console
# Run on every commit.
pre-commit install
```

#### On demand

If you want to run the checks on-demand (outside of git hooks), run:

```console
# Run on-demand.
pre-commit run --all-files
```

## FAQs

### Can I use `pip` to install this?

No. It is strictly a [`pre-commit`](http://pre-commit.com) hook.

### Is this project related to [`yamlfmt`](https://pypi.org/project/yamlfmt/)?

No.
