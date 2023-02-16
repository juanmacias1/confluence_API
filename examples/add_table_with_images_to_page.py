import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from pathlib import Path

from confluence.client import ConfluenceClient
from confluence.page import Page
from confluence.containers import Table, Image


client = ConfluenceClient.from_json_file("config.json")

# Retieve page object
page = Page.from_id(client, "603423014")


# Getting some image filepaths from a base folder
image_base_folder = Path("/mnt/toshiba_ssd/experimental/attachments")

# Attaching the images to the page. If the images are already attached, this updates the attachments.
# If the image are already attached to the page, you can skip this step.
files_to_attach = list(image_base_folder.iterdir())
page.attach_files(files_to_attach)

# Creating a table with the attached images
image_filenames = [img.name for img in files_to_attach]

# So far, only text and Image object containers are supported
table1_data = [
    ["", "Col1", "Col2", "Col3"],
    ["", Image(image_filenames[0]), "Nice text", "Much words"],
    ["", Image(image_filenames[2]), "Noch mehr Text", "Mais texto"],
]
my_table1 = Table(table1_data)

# Uploads the generated table to the page. CAREFUL: This overwrites the entire page content! (work TBD)
page.add_containers_to_body([my_table1])
