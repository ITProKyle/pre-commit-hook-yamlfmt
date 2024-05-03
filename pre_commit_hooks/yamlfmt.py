#! /usr/bin/env python3
"""Format YAML files."""
from __future__ import annotations

from pathlib import Path

import click
from ruamel.yaml import YAML

DEFAULT_COLONS: bool = False
DEFAULT_IMPLICIT_START: bool = True
DEFAULT_INDENT_MAPPING: int = 4
DEFAULT_INDENT_OFFSET: int = 4
DEFAULT_INDENT_SEQUENCE: int = 6
DEFAULT_PRESERVE_QUOTES: bool = True
DEFAULT_WIDTH: int = 4096


def format_yaml_file(yaml: YAML, file_path: Path) -> None:
    """Format the provided YAML file.

    Args:
        yaml: Configured instance of ``ruamel.yaml.YAML``.
        file_path: Path to a YAML file.

    """
    print(file_path, end="")  # noqa: T201
    yaml.dump_all(
        list(yaml.load_all(file_path)), file_path  # pyright: ignore[reportUnknownArgumentType]
    )
    print("  Done")  # noqa: T201


@click.command()
@click.option(
    "--colons/--no-colons",
    default=DEFAULT_COLONS,
    help="whether to align top-level colons",
    is_flag=True,
)
@click.option(
    "--implicit-start/--no-implicit-start",
    default=DEFAULT_IMPLICIT_START,
    help="whether to remove the explicit document start",
    is_flag=True,
)
@click.option(
    "--mapping",
    "-m",
    "indent_mapping",
    default=DEFAULT_INDENT_MAPPING,
    help="number of spaces to indent mappings (dictionaries)",
    type=int,
)
@click.option(
    "--offset",
    "-o",
    "indent_offset",
    default=DEFAULT_INDENT_OFFSET,
    help="number of spaces to offset the dash from sequences",
    type=int,
)
@click.option(
    "--sequence",
    "-s",
    "indent_sequence",
    default=DEFAULT_INDENT_SEQUENCE,
    help="number of spaces to indent sequences (arrays/lists)",
    type=int,
)
@click.option(
    "--preserve-quotes/--no-preserve-quotes",
    default=DEFAULT_PRESERVE_QUOTES,
    help="whether to keep existing string quoting",
    is_flag=True,
)
@click.option(
    "--width", "-w", "max_width", default=DEFAULT_WIDTH, help="maximum line width", type=int
)
@click.argument(
    "file_paths",
    nargs=-1,
    type=click.Path(
        dir_okay=False,
        exists=True,
        file_okay=True,
        path_type=Path,
        readable=True,
        resolve_path=True,
        writable=True,
    ),
)
def cli(  # noqa: PLR0913
    *,
    colons: bool,
    file_paths: tuple[Path, ...],
    implicit_start: bool,
    indent_mapping: int,
    indent_offset: int,
    indent_sequence: int,
    max_width: int,
    preserve_quotes: bool,
) -> None:
    """yamlfmt pre-commit hook.

    Documentation for the YAML parser used: https://yaml.readthedocs.io/en/latest/

    """
    yaml = YAML(pure=True, typ="rt")
    yaml.allow_unicode = True
    yaml.explicit_start = not implicit_start
    yaml.map_indent = indent_mapping
    yaml.preserve_quotes = preserve_quotes
    yaml.sequence_dash_offset = indent_offset
    yaml.sequence_indent = indent_sequence
    yaml.top_level_colon_align = colons  # pyright: ignore[reportAttributeAccessIssue]
    yaml.width = max_width

    for file_path in file_paths:
        format_yaml_file(yaml, file_path)


if __name__ == "__main__":
    cli.main()
