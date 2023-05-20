import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from pathlib import Path

from confluence.client import ConfluenceClient
from confluence.page import Page


client = ConfluenceClient.from_json_file("config.json")

page = Page.from_id(client, "603423014")
image_base_folder = Path("/mnt/toshiba_ssd/experimental/attachments")
files_to_attach = image_base_folder.iterdir()
page.attach_files(files_to_attach)
