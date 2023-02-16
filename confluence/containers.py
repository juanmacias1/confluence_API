from abc import ABC

from jinja2 import FileSystemLoader, Environment

JINJA_ENV = Environment(loader=FileSystemLoader("templates"))


class Container(ABC):
    def __init__(self, template_file_path: str):
        self.template = JINJA_ENV.get_template(template_file_path)


class Image(Container):
    def __init__(self, filename: str, template_file_path: str = "Image.j2"):
        super().__init__(template_file_path)
        self.filename = filename

    def __repr__(self) -> str:
        return self.render()

    def render(self):
        return self.template.render(filename=self.filename)


class Table(Container):
    def __init__(self, template_file_path: str = "Table.j2"):
        super().__init__(template_file_path)
        self.rows = []

    @classmethod
    def from_data(cls, rows):
        table = cls()
        table.rows = rows
        return table

    def add_header(self, header):
        self.rows.insert(0, header)

    def add_row(self, row):
        self.rows.append(row)

    def render(self):
        return self.template.render(rows=self.rows)
