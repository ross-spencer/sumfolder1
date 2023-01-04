"""Handler classes for DROID-style CSV files."""

import csv
from io import StringIO


class DROIDCSVException(Exception):
    """If there are issues handling the DROID CSV we can use this
    exception to provide more tailored feedback.
    """


class GenericCSVHandler:
    """Handler for generic CSV files."""

    def csv_from_string(self, droid_csv: str) -> list[dict]:
        """Read an IOStream object and return it as a CSV list."""
        csv_file = StringIO(droid_csv)
        csv_reader = csv.reader(csv_file)
        return self._process_csv(csv_reader)

    def csv_from_file(self, csv_name: str) -> list[dict]:
        """Return CSV rows as dictionaries in a list."""
        with open(csv_name, "r", encoding="UTF-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            return self._process_csv(csv_reader)

    @staticmethod
    def _process_csv(csv_reader: csv.reader) -> list[dict]:
        """Process a csv_reader object and return a list."""
        column_count = 0
        csv_list = []
        for row in csv_reader:
            if csv_reader.line_num == 1:
                header_list = row
                column_count = len(header_list)
                continue
            csv_dict = {}
            for idx in range(column_count):
                csv_dict[header_list[idx]] = row[idx]
            csv_list.append(csv_dict)
        return csv_list


class DROIDCSVHandler:
    """Class for working with DROID CSV files"""

    def __init__(self):
        """DROIDCSVHandler constructor."""
        self.hash = None
        self.csv = None

    def _set_hash(self, row: dict) -> None:
        """Set the global hash used by this DROID-style CSV. E.g. when
        DROID used MD5 this hash will come from MD5_HASH so MD5 is the
        value we will set.
        """
        for key, _ in row.items():
            if key.endswith("_HASH"):
                self.hash = key
                break
        if not hasattr(self, "hash"):
            raise ValueError("Script requires a CSV with HASH values set")

    def _get_hash(self):
        """Set the DROID CSV object's hash based on the DROID input."""
        try:
            self._set_hash(self.csv[0])
        except IndexError as err:
            raise DROIDCSVException(
                f"Problem accessing DROID CSV data: '{err}', csv_len: '{len(self.csv)}'"
            ) from IndexError

    def read_droid_csv_from_file(self, droid_csv_name: str) -> list[dict]:
        """Reads a DROID-style CSV using the Generic CSV handler
        class and sets the hash used in the report.
        """
        csv_handler = GenericCSVHandler()
        self.csv = csv_handler.csv_from_file(droid_csv_name)
        self._get_hash()
        return self.csv

    def read_droid_csv_from_string(self, droid_csv: str) -> list[dict]:
        """Reads a DROID-style CSV using an IO interface."""
        csv_handler = GenericCSVHandler()
        self.csv = csv_handler.csv_from_string(droid_csv)
        self._get_hash()
        return self.csv
