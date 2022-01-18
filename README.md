# YAML formatter for pre-commit git hooks

> This repo is a fork of [jumanjihouse/pre-commit-hook-yamlfmt](https://github.com/jumanjihouse/pre-commit-hook-yamlfmt).

YAML formatter for [pre-commit](http://pre-commit.com).

This hook formats the indentation of YAML files and optionally aligns top-level colons.

It uses [ruamel.yaml](https://yaml.readthedocs.io/en/latest/) to do the heavy lifting and preserve comments within YAML files.

## Arguments

- `--colons/--no-colons`: Whether to align top-level colons. _(default: `--no-colons`)_
- `--implicit-start/--no-implicit-start`: Whether to remove explicit document start. _(default: `--implicit-start`)_
- `-m, --mapping`: Number of space io indent mappings. _(default: `--mappings 4`)_
- `-o, --offset`: Number of space to offset the dash (`-`) from sequences. _(default: `--offset 4`)_
- `--preserve-quotes/--no-preserve-quotes`: Whether to keep existing string quotes. _(default: `--preserve-quotes`)_
- `-s, --sequence`: Number of space to indent sequences. _(default: `--sequence 6`)_
- `-w, --width`: Maximum line width. _(default: `--width 150`)_

## How-to

### Configure pre-commit

#### Use defaults

Add to `.pre-commit-config.yaml` in your git repo:

```yaml
- repo: https://github.com/ITProKyle/pre-commit-hook-yamlfmt
  rev: v0.2.0  # or specific tag
  hooks:
    - id: yamlfmt
```

:bulb: If a pre-commit hook changes a file, the hook fails with a warning that files were changed.

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
  rev: v0.2.0  # or specific tag
  hooks:
    - id: yamlfmt
```

#### Override defaults

Add to `.pre-commit-config.yaml` in your git repo:

```yaml
- repo: https://github.com/ITProKyle/pre-commit-hook-yamlfmt
  rev: v0.2.0  # or specific tag
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
