import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from confluence.client import ConfluenceClient
from confluence.page import Page
from confluence.elements import Space

# Initializing the client
client = ConfluenceClient.from_json_file("config.json")

# Creating a page object
MY_SPACE_KEY = "~62c43b6e580f2f55d76fefd9"
my_space = Space(key=MY_SPACE_KEY)
page = Page.create(client, "Test Page 3 - API generated", my_space)

print(page.get_title())
print(page.get_version())
