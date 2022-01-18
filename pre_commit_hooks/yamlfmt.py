#! /usr/bin/env python3
"""Format YAML files."""
from __future__ import annotations

import argparse
import locale
import sys
from dataclasses import asdict, dataclass, field
from functools import cached_property
from typing import TYPE_CHECKING, Any, List, NoReturn

from ruamel.yaml import YAML

if TYPE_CHECKING:
    from _typeshed import StrPath


DEFAULT_COLONS = False
DEFAULT_IMPLICIT_START = True
DEFAULT_INDENT_MAPPING = 4
DEFAULT_INDENT_OFFSET = 4
DEFAULT_INDENT_SEQUENCE = 6
DEFAULT_PRESERVE_QUOTES = True
DEFAULT_WIDTH = 150


@dataclass
class Args:
    """Hook arguments."""

    colons: bool = DEFAULT_COLONS
    file_names: List[str] = field(default_factory=list)
    implicit_start: bool = DEFAULT_IMPLICIT_START
    mapping: int = DEFAULT_INDENT_MAPPING
    offset: int = DEFAULT_INDENT_OFFSET
    preserve_quotes: bool = DEFAULT_PRESERVE_QUOTES
    sequence: int = DEFAULT_INDENT_SEQUENCE
    width: int = DEFAULT_WIDTH


class Cli:
    """Command line interface."""

    def __init__(self) -> None:
        """Instantiate class."""
        parser = argparse.ArgumentParser(
            description="Format YAML files",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            epilog="Tips at https://yaml.readthedocs.io/en/latest/detail.html",
        )
        parser.add_argument(
            "-m",
            "--mapping",
            type=int,
            default=DEFAULT_INDENT_MAPPING,
            help="number of spaces to indent mappings (dictionaries)",
        )
        parser.add_argument(
            "-s",
            "--sequence",
            type=int,
            default=DEFAULT_INDENT_SEQUENCE,
            help="number of spaces to indent sequences (arrays/lists)",
        )
        parser.add_argument(
            "-o",
            "--offset",
            type=int,
            default=DEFAULT_INDENT_OFFSET,
            help="number of spaces to offset the dash from sequences",
        )
        parser.add_argument(
            "--colons",
            action="store_const",
            const=True,
            default=DEFAULT_COLONS,
            dest="preserve_quotes",
            help="whether to align top-level colons",
        )
        parser.add_argument(
            "--no-colons",
            action="store_const",
            const=False,
            dest="preserve_quotes",
            help="whether to align top-level colons",
        )
        parser.add_argument(
            "-w",
            "--width",
            type=int,
            default=DEFAULT_WIDTH,
            help="maximum line width",
        )
        parser.add_argument(
            "--preserve-quotes",
            action="store_const",
            const=True,
            default=DEFAULT_PRESERVE_QUOTES,
            dest="preserve_quotes",
            help="whether to keep existing string quoting",
        )
        parser.add_argument(
            "--no-preserve-quotes",
            action="store_const",
            const=False,
            dest="preserve_quotes",
            help="whether to keep existing string quoting",
        )
        parser.add_argument(
            "--implicit-start",
            action="store_const",
            const=True,
            default=DEFAULT_IMPLICIT_START,
            dest="implicit_start",
            help="whether to remove the explicit document start",
        )
        parser.add_argument(
            "--no-implicit-start",
            action="store_const",
            const=False,
            dest="implicit_start",
            help="whether to remove the explicit document start",
        )
        parser.add_argument(
            "file_names",
            metavar="FILE_NAME",
            nargs="*",
            help="space-separated list of YAML file names",
        )
        self.parser = parser

    @cached_property
    def args(self) -> Args:
        """CLI arguments."""
        return Args(**self.parser.parse_args().__dict__)


class Formatter:
    """Reformat a yaml file with proper indentation. Preserve comments."""

    def __init__(
        self,
        colons: bool = DEFAULT_COLONS,
        implicit_start: bool = DEFAULT_IMPLICIT_START,
        mapping: int = DEFAULT_INDENT_MAPPING,
        offset: int = DEFAULT_INDENT_OFFSET,
        preserve_quotes: bool = DEFAULT_PRESERVE_QUOTES,
        sequence: int = DEFAULT_INDENT_SEQUENCE,
        width: int = DEFAULT_WIDTH,
        **__kwargs: Any,
    ) -> None:
        """Instantiate class."""
        yaml = YAML()
        yaml.indent(
            mapping=mapping,
            sequence=sequence,
            offset=offset,
        )
        yaml.top_level_colon_align = colons
        yaml.explicit_start = not implicit_start
        yaml.width = width
        yaml.preserve_quotes = preserve_quotes

        self.yaml = yaml
        self.content = list({})

    def format(self, path: StrPath) -> None:
        """Read file and write it out to same path."""
        print(path, end="")
        self.parse_file(path)
        self.write_file(path)
        print("  Done")

    def parse_file(self, path: StrPath) -> None:
        """Read the file."""
        try:
            with open(
                path, "r", encoding=locale.getpreferredencoding(do_setlocale=False)
            ) as stream:
                self.content = list(self.yaml.load_all(stream))  # type: ignore
        except IOError:
            self.fail(f"Unable to read {path}")

    def write_file(self, path: StrPath) -> None:
        """Write the file."""
        try:
            with open(
                path, "w", encoding=locale.getpreferredencoding(do_setlocale=False)
            ) as stream:
                self.yaml.dump_all(self.content, stream)
        except IOError:
            self.fail(f"Unable to write {path}")

    @staticmethod
    def fail(msg: str) -> NoReturn:
        """Abort."""
        sys.stderr.write(msg)
        sys.exit(1)


def main() -> None:
    """Execute module."""
    cli = Cli()
    formatter = Formatter(**asdict(cli.args))
    for file_name in cli.args.file_names:
        formatter.format(file_name)


if __name__ == "__main__":
    main()
