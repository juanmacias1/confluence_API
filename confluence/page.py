from __future__ import annotations

import json
from typing import Optional, Iterable

from .elements import Space, Version


class Page:
    def __init__(
        self,
        confluence_client: ConfluenceClient,
        id: str,
        title: Optional[str] = None,
        space: Optional[Space] = None,
        version: Optional[Version] = None,
    ):
        self.confluence_client = confluence_client
        self.id = id
        self._title = title
        self._version = version
        self._space = space
        self._is_fetched = False

    @classmethod
    def from_id(cls, confluence_client: ConfluenceClient, id: str) -> Page:
        return cls(confluence_client, id)

    @classmethod
    def create(
        cls,
        confluence_client: ConfluenceClient,
        title: str,
        space: Space,
    ) -> "Page":
        # Creates page on confluence and returns an object representing the page
        content = confluence_client.create_page(title, space)
        return cls(
            confluence_client,
            content["id"],
            title=title,
            space=space,
            version=Version(**content["version"]),
        )

    def add_containers_to_body(self, containers: Iterable[Container]) -> dict:
        if not self._is_fetched:
            self._fetch()

        self._version.increment()
        ### This kind of stuff should be handlded by the ConfluenceClient class. But it works so far ###
        payload = {
            "version": self._version.dict(),
            "title": self._title,
            "type": "page",
            "space": self._space.dict(),
            "body": {
                "storage": {
                    "value": "".join(container.render() for container in containers),
                    "representation": "storage",
                }
            },
        }
        return self.confluence_client._make_request(
            "PUT", self.confluence_client.base_url + self.id, json.dumps(payload)
        )
        ####################################################################

    def attach_files(self, files: Iterable[Path]) -> dict:
        # TBD: Add optional caching
        return self.confluence_client.attach_files_to_page(self.id, files)

    def get_attachments(self) -> dict:
        return self.confluence_client.get_page_attachments_list(self.id)

    def _fetch(self) -> None:
        self._page = self.confluence_client.get_page(self.id)
        self._title = self._page["title"]
        self._version = Version(**self._page["version"])
        self._space = Space(**self._page["space"])
        self._is_fetched = True

    def _get_property(self, property_name: str):
        if not getattr(self, property_name):
            self._fetch()
        return getattr(self, property_name)

    def get_title(self) -> Space:
        return self._get_property("_title")

    def get_space(self) -> Space:
        return self._get_property("_space")

    def get_version(self) -> int:
        return self._get_property("_version")
