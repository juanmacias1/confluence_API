
README

This script is used to interact with the Confluence API to perform actions on pages such as getting page information, creating an empty page, and updating a page. The script utilizes the requests library to make API calls and argparse to handle command-line arguments.

Command-Line Arguments

The following command-line arguments are required to use the script:

    -e or --email : The email address associated with your Confluence account
    -t or --token : The API token for your Confluence account

The following command-line arguments are used to specify the action to be performed:

    -m or --mode : The action to be performed, one of get_page_info, create_page, update_page.
    --page-id : The ID of the page on which the action is to be performed. Required for get_page_info, update_page.
    --page-title : The title of the page to be created. Required for create_page.
    --space-id : The ID of the space in which the page is to be created. Required for create_page.
    --space-key : The key of the space in which the page is to be created. Required for create_page.
    --ancestor-id : The ID of the parent page. Required for create_page, update_page.
    --action : The action to be performed on the page. Required for update_page. One of create_table, attach_files.
    --rows-number : Number of rows in the table to be created. Required for create_table.
    --columns-number : Number of columns in the table to be created. Required for create_table.
    --file : File or directory of files to be attached. Required for attach_files.
    --orientation, --insert-at: Orientation and column or row number where the files will be generated (required for create_table_with_images action)

The script also uses the requests library to make HTTP requests to the Confluence REST API, and the json library to parse the JSON responses from the API.

The script consists of a class called HTTPClient, which defines methods to perform the different actions that the script can perform:

Examples

Get page information:

python3 get_create_update.py -e <your-navvis-email@navvis.com> -t <Your_API_Token> --mode get_page_info --page-id 545587201

Create an empty page:

python3 get_create_update.py -e <your-navvis-email@navvis.com> -t <Your_API_Token> --mode create_page --page-title NEWSCRIPTWORKS --space-id 334004387 --space-key MAP --ancestor-id 545587201

Update page by creating a table:

python3 get_create_update.py -e <your-navvis-email@navvis.com> -t <Your_API_Token> --mode update_page --page-id 568951834 --action create_table --ancestor-id 545587201 --rows-number 5 --columns-number 2

Update page by attaching a single file:

python3 get_create_update.py -e <your-navvis-email@navvis.com> -t <Your_API_Token> --mode update_page --action attach_files --page-id 560496957 --ancestor-id 545587201 

Update page by adding table with images

python3 get_create_update.py -e <your-navvis-email@navvis.com> -t <Your_API_Token> --mode update_page --action create_table_with_images  --page-id 568951834 --ancestor-id 545587201 --rows-number 10 --columns-number 2 --file /home.net/ja21xis/Downloads/cats --orientation V --insert-at 1
