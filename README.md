<!DOCTYPE html>
<html>
  <head>
    <title>README</title>
  </head>
  <body>
    <a href="#about-the-project">About The Project</a>
    <p>This script is used to interact with the Confluence API to perform actions on pages such as getting page information, creating an empty page, and updating a page. The script utilizes the requests library to make API calls and argparse to handle command-line arguments.</p>
    <h2>Command-Line Arguments</h2>
    <p>The following command-line arguments are required to use the script:</p>
    <ul>
      <li>-e or --email : The email address associated with your Confluence account</li>
      <li>-t or --token : The API token for your Confluence account</li>
    </ul>
    <p>The following command-line arguments are used to specify the action to be performed:</p>
    <ul>
      <li>-m or --mode : The action to be performed, one of get_page_info, create_page, update_page.</li>
      <li>--page-id : The ID of the page on which the action is to be performed. Required for get_page_info, update_page.</li>
      <li>--page-title : The title of the page to be created. Required for create_page.</li>
      <li>--space-id : The ID of the space in which the page is to be created. Required for create_page.</li>
      <li>--space-key : The key of the space in which the page is to be created. Required for create_page.</li>
      <li>--ancestor-id : The ID of the parent page. Required for create_page, update_page.</li>
      <li>--action : The action to be performed on the page. Required for update_page. One of create_table, attach_files.</li>
      <li>--rows-number : Number of rows in the table to be created. Required for create_table.</li>
      <li>--columns-number : Number of columns in the table to be created. Required for create_table.</li>
      <li>--file : File or directory of files to be attached. Required for attach_files.</li>
      <li>--orientation, --insert-at: Orientation and column or row number where the files will be generated (required for create_table_with_images action)</li>
    </ul>
    <p>The script also uses the requests library to make HTTP requests to the Confluence REST API, and the json library to parse the JSON responses from the API.</p>
    <p>The script consists of a class called HTTPClient, which defines methods to perform the different actions that the script can perform:</p>
    <h2>Examples</h2>
    <p>Get page information:</p>
    <pre>python3 get_create_update.py -e &lt;your-navvis-email@navvis.com&gt; -t &lt;Your_API_Token&gt; --mode get_page_info --page-id 545587201</pre>
    <p>Create an empty page:</p>
    <pre>python3 get_create_update.py -e &lt;
