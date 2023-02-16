from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Optional, Iterable, Union

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

REQUEST_EXPANSIONS = ["body.storage", "version", "space"]
EXPANSION_SUFFIX = "?expand=" + ",".join(REQUEST_EXPANSIONS)

# Header used in almost all requests
STANDARD_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# Header used in multipart/form-data requests
BOUNDARY = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
MULTIPART_CONTENT_HEADERS = {
    "Content-Type": "multipart/form-data; boundary=" + BOUNDARY,
    "X-Atlassian-Token": "nocheck",
}


class Credentials:
    def __init__(self, email: str, token: str):
        self.email = email
        self.token = token

    @staticmethod
    def from_json(json_data: dict) -> Credentials:
        return Credentials(json_data["email"], json_data["token"])


@dataclass
class ConfluenceClient:
    credentials: Credentials
    base_url: str

    def __post_init__(self):
        self.auth = HTTPBasicAuth(self.credentials.email, self.credentials.token)
        self.content_base_url = self.base_url + "content/"

    @staticmethod
    def from_json_file(json_filepath: str) -> ConfluenceClient:
        with open(json_filepath) as f:
            json_data = json.load(f)
        return ConfluenceClient(
            Credentials.from_json(json_data["credentials"]),
            json_data["base_url"],
        )

    def create_page(self, page_title: str, page_space: Space) -> Page:
        data = {
            "type": "page",
            "title": page_title,
            "space": page_space.dict(),
        }

        # Creates page on confluence and returns an object representing the page
        content = self._make_request("POST", self.content_base_url, json.dumps(data))
        return content

    def get_page(self, page_id: str) -> dict:
        url = self.content_base_url + page_id + EXPANSION_SUFFIX
        return self._make_request("GET", url)

    def get_page_attachments_list(self, id):
        url = self.content_base_url + id + "/child/attachment"
        data = self._make_request("GET", url)
        attachment_list = []
        for attachment in data["results"]:
            attachment_list.append(attachment["title"])
        return attachment_list

    def attach_files_to_page(self, page_id: str, filepaths: Iterable[Path]) -> dict:
        def _make_multipart_data(filepath: Path) -> bytes:
            with open(filepath, "rb") as f:
                data = f.read()

            multipart_data_begin = (
                f"--{BOUNDARY}\r\nContent-Disposition: form-data;"
                f'name="file"; filename="{filepath.name}"\r\n\r\n'
            )
            return (
                multipart_data_begin.encode()
                + data
                + f"\r\n--{BOUNDARY}--\r\n".encode()
            )

        # This is also ugly and shouldn't be hardcoded
        url = self.content_base_url + page_id + "/child/attachment"
        for filepath in filepaths:
            multipart_data = _make_multipart_data(filepath)
            logging.debug(f"Attempting to attach file {filepath} to page {page_id}")
            self._make_request(
                "PUT", url, data=multipart_data, headers=MULTIPART_CONTENT_HEADERS
            )
            logging.info(f"File {filepath} attached to page {page_id}")

    def _make_request(
        self,
        method: str,
        url: str,
        data: Optional[Union[bytes, dict]] = None,
        headers: Optional[dict] = None,
    ) -> dict:
        if headers is None:
            headers = STANDARD_HEADERS

        logging.debug(f"Attempting {method} request to {url}")
        response = requests.request(
            method,
            url=url,
            headers=headers,
            auth=self.auth,
            data=data,
        )
        # Check response status code
        if response.status_code != 200:
            error_msg = f"Request to {url} with data {data} and method {method} failed with status code {response.status_code} - Response text: {response.text}"
            logging.error(error_msg)
            raise RequestException(error_msg)

        logging.info("Success!")
        return json.loads(response.text)
