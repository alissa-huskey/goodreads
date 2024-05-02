"""CLI for goodreads app."""

from pathlib import Path
from sys import argv, exit

from rich import print
from rich.table import Table
from rich.traceback import install as rich_tracebacks
from typer import Argument, Option, Typer
from typing_extensions import Annotated

from gr.csv_file import CsvFile

cli = Typer()
rich_tracebacks(show_locals=True, max_frames=10)
bp = breakpoint


def process_fields(value: list):
    """Split up comma-seperated fields into list."""
    if len(value) == 1 and "," in (fields := value[0]):
        value = list(map(str.strip, fields.split(",")))
    return value


@cli.command()
def readfile(
    path: Annotated[Path, Argument(help="path to CSV file")],
    fields: Annotated[list[str], Option(
        callback=process_fields,
        help="fields to display",
    )] = [],
    list_fields: Annotated[bool, Option(help="list header fields in file")] = False,
    goodreads: Annotated[bool, Option(help="this is a goodreads file")] = False,
):
    """Read a CSV file and display all or a select group of fields to display."""
    file = CsvFile(path)
    file.read()

    if not file:
        print("Empty.")
        return

    if list_fields:
        row = file[0]
        for field in row.keys():
            print(field)
        if goodreads:
            print("Shelved")
        return

    if goodreads:
        fields = fields or ["Title", "Author", "Shelved"]
    else:
        fields = fields or file[0].keys()

    table = Table(*fields)

    for row in file:
        if goodreads:
            shelves = row["Shelves"] and [row["Shelves"]] or []
            all_shelves = shelves + row["Bookshelves"].split()
            row["Shelved"] = ", ".join(all_shelves)

        table.add_row(*map(row.get, fields))

    print(table)


def run():
    try:
        cli()
    except SystemExit:
        ...


if __name__ == "__main__":
    cli()
