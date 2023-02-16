import pprint
from collections import deque
from abc import ABC
from typing import List, Iterable, Optional

from jinja2 import FileSystemLoader, Environment

JINJA_ENV = Environment(loader=FileSystemLoader("templates"))


class Container(ABC):
    def __init__(self, template_file_path: str):
        self.template = JINJA_ENV.get_template(template_file_path)


class Image(Container):
    def __init__(self, filename: str, template_file_path: str = "Image.j2"):
        super().__init__(template_file_path)
        self.filename = filename

    def __str__(self) -> str:
        return self.render()

    def render(self):
        return self.template.render(filename=self.filename)


class Deque(deque):
    def __repr__(self):
        return pprint.pformat(list(self))


class Table(Container):
    def __init__(
        self,
        rows: Optional[List] = None,
        template_file_path: str = "Table.j2",
    ):
        super().__init__(template_file_path)

        if not rows:
            self.rows: Deque = Deque()
            self._nrows = 0
            self._ncols = 0
            return

        # Checking table structure
        self._nrows = len(rows)
        self._ncols = len(rows[0])
        assert (
            len(set(len(row) for row in rows)) == 1
        ), "All rows must have the same number of columns!!"

        # Converting all rows and inner elements to deques
        self.rows: Deque = Deque(Deque(row) for row in rows)

    def __repr__(self):
        return pprint.pformat(self.rows)

    def __getitem__(self, ix):
        if isinstance(ix, tuple):
            i, j = ix
            return self.rows[i][j]
        return self.rows[ix]

    def __setitem__(self, ix, value):
        i, j = ix
        self.rows[i][j] = value

    def append_row(self, row):
        assert (
            len(row) == self._ncols
        ), f"Row must have the same number of columns as the current table, which is {self._ncols}. Passed row has {len(row)} columns."
        self.rows.append(Deque(row))
        self._nrows += 1

    def append_column(self, column):
        assert (
            len(column) == self._nrows
        ), f"Column must have the same number of rows as the current table, which is {self._nrows}. Passed column has {len(column)} rows."
        for i, row in enumerate(self.rows):
            row.append(column[i])
        self._ncols += 1

    def prepend_row(self, row):
        assert (
            len(row) == self._ncols
        ), f"Row must have the same number of columns as the current table, which is {self._ncols}. Passed row has {len(row)} columns."
        self.rows.appendleft(Deque(row))
        self._nrows += 1

    def prepend_column(self, column):
        assert (
            len(column) == self._nrows
        ), f"Column must have the same number of rows as the current table, which is {self._nrows}. Passed column has {len(column)} rows."
        for i, row in enumerate(self.rows):
            row.appendleft(column[i])
        self._ncols += 1

    @property
    def size(self) -> tuple:
        return self._nrows, self._ncols

    @property
    def nrows(self) -> int:
        return self._nrows

    @property
    def ncols(self) -> int:
        return self._ncols

    def render(self):
        return self.template.render(rows=self.rows)
