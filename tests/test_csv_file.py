from gr.csv_file import CsvFile
from pathlib import Path

def test_csv_file(datadir):

    filepath = datadir / "sample_export.csv"
    file = CsvFile(filepath)

    assert isinstance(file, CsvFile)
    assert file.filepath == filepath

def test_read(datadir):
    """
    GIVEN: A path pointing to a csv file
    WHEN: The CsvFile is created with that path
    THEN: The object should act as a list where each item is a row
    AND: Each row is a dict-like object
    AND: The first row in the file is the headers (keys) and ommitted from items
    """

    filepath = datadir / "sample_export.csv"
    file = CsvFile(filepath)
    file.read()

    assert len(file) == 5

    book = file[1]
    assert book["Title"] == "Blink: The Power of Thinking Without Thinking"

def test_read_strip(datadir):
    """
    GIVEN: A csv file with trailing spaces between commas
    WHEN: The file is read
    THEN: The row dict keys and values should be stripped of spaces.
    """

    filepath = datadir / "sample_export.csv"
    file = CsvFile(filepath)
    file.read()

    assert len(file) == 5

    book = file[0]
    assert book["Author"] == "arthur golden"
