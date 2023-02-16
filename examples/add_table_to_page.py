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

# Mocking some table data and addng to page
table1_data = [
    ["", "A", "B", "C"],
    ["1", "A1", "B1", "C1"],
    ["2", "A2", "B2", "C2"],
]
my_table1 = Table.from_data(table1_data)
my_table1.add_header(["C1", "C2", "C3", "C4"])
table2_data = [
    ["", "A", "B", "C"],
    ["1", "A1", "B1", "C1"],
    ["2", "A2", "B2", "C2"],
    ["2", "A2", "B2", "C2"],
    ["2", "A3", "B3", "C3"],
    ["2", "A2", "B2", "C2"],
]
my_table2 = Table.from_data(table2_data)
my_table2.add_header(["C1", "C2", "C3", "C4"])
page.add_containers_to_body([my_table1, my_table2])
