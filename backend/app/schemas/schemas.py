from pydantic import BaseModel, Field, HttpUrl

from ..utils import Summary


class User(BaseModel):
    name: str


class SummaryResponse(Summary):
    picture_url: HttpUrl = Field(description="A profile picture URL")
