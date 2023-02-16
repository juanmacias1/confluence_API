import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from confluence.client import ConfluenceClient
from confluence.page import Page
from confluence.containers import Table


# Initializing the client
client = ConfluenceClient.from_json_file("config.json")

# Fetching page data
page = Page.from_id(client, "603423014")

# Mocking some table data
table1_data = [
    ["", "A", "B", "C"],
    ["1", "A1", "B1", "C1"],
    ["2", "A2", "B2", "C2"],
]
my_table1 = Table(table1_data)

# Appending rows to the table
my_table1.append_row(["3", "A3", "B3", "C3"])
my_table1.append_row([42] * my_table1.ncols)

# Adding columns
my_table1.append_column(["D", "D1", "D2", "D3", "D4"])
my_table1.prepend_column(["E", "E1", "E2", "E3", "E4"])

# Adding a header with column names
header = [f"Column {i}" for i in range(my_table1.ncols)]
my_table1.prepend_row(header)

# Adding a footer with column names
footer = [f"Footer {i}" for i in range(my_table1.ncols)]
my_table1.append_row(footer)

# Accessing a table element
print(my_table1[1, 2])

# Setting a table element
my_table1[1, 2] = 424242
print(my_table1[1, 2])

# Pushing table to the confluence page (you can pass more than one table in the list argument, if you want)
page.add_containers_to_body([my_table1])
