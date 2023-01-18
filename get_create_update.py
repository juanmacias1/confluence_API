import requests
from requests.auth import HTTPBasicAuth
import argparse
import json
from jinja2 import Template
import os
from actions import generate_table
from actions import generate_table_with_images


class HTTPClient:
    def __init__(self, base_url, auth, headers):
        self.base_url = base_url
        self.auth = auth
        self.headers = headers

    def get_page_info(self, id):        
        response = requests.request(
        "GET",
        url=self.base_url+id,
        headers=self.headers,
        auth=self.auth
        )
        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    def return_page_info(self, id):        
        response = requests.request(
        "GET",
        url=self.base_url+id,
        headers=self.headers,
        auth=self.auth
        )
        return response
        
    def get_version(self,id):
        response = requests.request(
        "GET",
        url=self.base_url+id+"?expand=version",
        headers=self.headers,
        auth=self.auth
        )
        data = json.loads(response.text)
        version_number = data["version"]["number"]
        return version_number

    def get_page_title(self,id):
        response = requests.request(
        "GET",
        url=self.base_url+id,
        headers=self.headers,
        auth=self.auth
        )
        data = json.loads(response.text)
        title = data["title"]
        return title

    def get_space_info(self,id):
        response = requests.request(
        "GET",
        url=self.base_url+id,
        headers=self.headers,
        auth=self.auth
        )
        data = json.loads(response.text)
        space_id = data["space"]["id"]
        space_key = data["space"]["key"]
        space_info = space_id,space_key
        return space_info

    def create_page(self, title, space_id, space_key, ancestor):    
            
        payload = json.dumps({
            "title": "{0}".format(title),
            "type": "page",
            "space": {
                "id": space_id,
                "key": "{0}".format(space_key),
                "type": "global",
                "status": "current"
            },
            "status": "current",
            "ancestors": [
                {
                    "id": ancestor
                }
            ]
        })
        
        response = requests.request(
            "POST",
            url=self.base_url,
            data=payload,
            headers=self.headers,
            auth=self.auth
        )
        #Uncomment the following line to read further details.
        #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        if response.status_code == 200:
            print("[OK] Confluence page created.")
        else:
            print("[ERROR] Status code is: {0}".format(response.status_code))

    def create_empty_table(self, id, ancestor, size):
        page_version = client.get_version(id)
        page_title = client.get_page_title (id)
        space_info = client.get_space_info(id)
        generated_table = generate_table(size[0], size[1])

        payload = json.dumps({
            "version": {
                "number": page_version + 1
            },
            "title": "{0}".format(page_title),
            "type": "page",
            "space": {
                "id": space_info[0],
                "key": "{0}".format(space_info[1]),
                "type": "global",
                "status": "current"
            },
            "status": "current",
            "ancestors": [
                {
                    "id": ancestor
                }
            ],
                "body": {
                    "storage": {
                        "value": "{0}".format(generated_table),
                        "representation": "storage"
                    }
                }
        })
        response = requests.request(
        "PUT",
        url=self.base_url+id,
        data=payload,
        headers=self.headers,
        auth=self.auth
        )

        #To read the full response:
        #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        if response.status_code == 200:
            print("[OK] Confluence page updated with table.")
        else:
            print("[ERROR] Status code is: {0}".format(response.status_code))
      
    def attach_files(self, id, file):
        attached_files=client.get_attachments_list(id)
        if not attached_files:
            print("NO files to attach.")
        else:
            page_info = client.return_page_info(id)

            files_to_upload = []
            if os.path.isdir(file):
                # If a directory is provided, get all files in the directory
                for root, dirs, files in os.walk(file):
                    for file in files:
                        files_to_upload.append(os.path.join(root, file))
            else:
            #If a file is provided, add it to the list of files to upload
                files_to_upload.append(file)

            boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
            headers = {
                'Content-Type': 'multipart/form-data; boundary='+boundary,
                'X-Atlassian-Token': 'nocheck'
            }
            
            content = json.loads(page_info.text)
            base_url = content["_links"]["base"]
            links = []
            for file_path in files_to_upload:
                # Get the file name
                file_name = os.path.basename(file_path)
                if file_name not in attached_files:
                    multipart_data_0 = f'--{boundary}\r\nContent-Disposition: form-data;' \
                                    f'name="file"; filename="{file_name}"\r\n\r\n'


                    multipart_data = multipart_data_0.encode() + open(file_path, 'rb').read() + f'\r\n--{boundary}--\r\n'.encode()

                    response = requests.post(
                        f'https://navvis.atlassian.net/wiki/rest/api/content/{id}/child/attachment',
                        auth=auth,
                        headers=headers,
                        data=multipart_data
                    )

                    data = json.loads(response.text)

                    file_link = data['results'][0]['_links']['download']
                    file_link = file_link.split('?')[0]
                    full_link = base_url + file_link
                    links.append(full_link)
                    print(f'File {file_name} uploaded successfully with link {full_link}')
                else:
                    print(f'File {file_name} previously attached.')
            print(links)
            return links

    def create_table_with_images(self, id, ancestor, file, size, orientation, insert_at):

        page_version = client.get_version(id)
        page_title = client.get_page_title (id)
        space_info = client.get_space_info(id)   
        print(page_version)
        file_links = client.attach_files(id, file)
        
        if not file_links:
            print("[FAILED] NO files to attach.")
        else: 
            html = generate_table_with_images(size[0], size[1], file_links, orientation, insert_at)
            
            payload = json.dumps({
                "version": {
                    "number": page_version + 1
                },
                "title": "{0}".format(page_title),
                "type": "page",
                "space": {
                    "id": space_info[0],
                    "key": "{0}".format(space_info[1]),
                    "type": "global",
                    "status": "current"
                },
                "status": "current",
                "ancestors": [
                    {
                        "id": ancestor
                    }
                ],
                    "body": {
                        "storage": {
                            "value": "{0}".format(html),
                            "representation": "storage"
                        }
                    }
            })
            response = requests.request(
            "PUT",
            url=self.base_url+id,
            data=payload,
            headers=self.headers,
            auth=self.auth
            )

            #To read the full response:
            #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
            if response.status_code == 200:
                print("[OK] Confluence page updated with table.")
            else:
                print("[ERROR] Status code is: {0}".format(response.status_code))

    def get_attachments_list(self, id):
        response = requests.request(
        "GET",
        url=self.base_url+id+"/child/attachment",
        headers=self.headers,
        auth=self.auth
        )
        data = json.loads(response.text)
        attachment_list = []
        for attachment in data["results"]:
            attachment_list.append(attachment["title"])
        
        return attachment_list




parser = argparse.ArgumentParser(description="Basic script for confluence rest API usage")
parser.add_argument("--email", "-e", dest="email", type=str, required=True, help="NavVis email for authentication")
parser.add_argument("--token", "-t", dest="token", type=str, required=True, help="API token for authentication")
parser.add_argument("--mode", "-m", dest="mode", type=str, required=True, help="Action to perform: 'get_page_info', 'create_page', or 'update_page'", choices=["get_page_info", "create_page", "update_page"])

# Arguments for get_page_info mode
parser.add_argument("--page-id", "-i", dest="page_id", type=str, required=False, help="ID of the page")

# Arguments for create_page and update page mode
parser.add_argument("--page-title", "-ti", dest="page_title", type=str, required=False, help="Title of the page to be created.")
parser.add_argument("--space-id", "-s", dest="space_id", type=str, required=False, help="Id of the space where the page will be created.")
parser.add_argument("--space-key", "-sk", dest="space_key", type=str, required=False, help="Key of the space where the page will be created.")
parser.add_argument("--ancestor-id", "-a", dest="ancestor_id", type=str, required=False, help="Id of the parent page to be created")

# Arguments for update_page mode
parser.add_argument("--action", "-act", dest="action", type=str, required=False, help="Flag to specify action.")

# Arguments for table generation
parser.add_argument("--rows-number", "-r", dest="rows_number", type=int, required=False, help="Flag to specify the number of rows of the generated table.")
parser.add_argument("--columns-number", "-c", dest="columns_number", type=int, required=False, help="Flag to specify the number of columns of the generated table.")

#Arguments for files attatchment
parser.add_argument("--file", "-f", dest="file", type=str, required=False, help="Absolute path of the file to attach.")

#Arguments for table with images
parser.add_argument("--orientation", "-o", dest="orientation", type=str, required=False, help="Add V for vertical or H for horizontal.")
parser.add_argument("--insert-at", "-ia", dest="insert_at", type=str, required=False, help="Flag to specify the column or row number where the files will be generated")


args = parser.parse_args()


if not args.email or not args.token or not args.mode:
    raise ValueError("email, token and mode are required arguments")
if args.mode == "get_page_info" and not args.page_id:
    raise ValueError("page_id is required when using get_page_info mode")
if args.mode == "create_page" and (not args.page_title or not args.space_id or not args.space_key or not args.ancestor_id):
    raise ValueError("page_title, space_id, space_key, and ancestor_id are required when using create_page mode")
if args.mode == "update_page" and args.action == "create_table" and (not args.page_id or not args.ancestor_id or not args.rows_number or not args.columns_number):
    raise ValueError("page_id, ancestor_id, and table_size are required when using update_page mode with create_table action")
if args.mode == "update_page" and args.action == "attach_files" and (not args.page_id or not args.file_path):
    raise ValueError("page_id and file_path are required when using update_page mode with attach_files action")
if args.mode == "update_page" and args.action == "create_table_with_images" and (not args.page_id or not args.ancestor_id or not args.file or not args.rows_number or not args.columns_number or (args.orientation not in ["V","H"]) or not (args.insert_at.isdigit())):
    raise ValueError("page_id, ancestor_id, file, rows_number, columns_number, orientation (V or H) and insert_at are required when using update_page mode with create_table_with_images action")


args = parser.parse_args()
email = args.email
token = args.token
mode = args.mode
page_id = args.page_id
page_title = args.page_title
space_id = args.space_id
space_key = args.space_key
ancestor_id = args.ancestor_id
action = args.action
rows_number = args.rows_number
columns_number = args.columns_number
table_size = (rows_number, columns_number)
file_path = args.file
orientation = args.orientation
insert_at = args.insert_at

base_url="https://navvis.atlassian.net/wiki/rest/api/content/"
auth = HTTPBasicAuth(email, token)
headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

client = HTTPClient(base_url, auth, headers)

if mode in ["get_page_info", "update_page"] and page_id is None:
    parser.error("--page-id is required for the 'get_page_info' and 'update_page' actions")
elif mode == "get_page_info":
    client.get_page_info(page_id)
elif mode == "create_page":
    client.create_page(page_title, space_id, space_key, ancestor_id)
elif mode == "update_page":
    if action == "create_table":
        client.create_empty_table(page_id, ancestor_id, table_size)
    elif action == "attach_files":
        client.attach_files(page_id, file_path)
    elif action == "create_table_with_images":
        client.create_table_with_images(page_id, ancestor_id, file_path, table_size, orientation, insert_at)
    
