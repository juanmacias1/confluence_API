from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class APIElement(BaseModel):
    @classmethod
    def from_dict(cls, data_dict: dict) -> APIElement:
        return cls(**data_dict)

    pass


class Version(APIElement):
    number: int
    message: Optional[str] = None

    def increment(self) -> None:
        self.number += 1


class Space(APIElement):
    key: str
