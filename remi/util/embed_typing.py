from typing import Optional, Any, Iterable
import datetime
from hikari import colors, files
from typing import TypedDict


class EmbedAuthor(TypedDict):
    name: Optional[str]
    url: Optional[str]
    icon: Optional[files.Resourceish]


class EmbedFooter(TypedDict):
    text: Optional[str]
    icon: Optional[files.Resourceish]


class EmbedField(TypedDict):
    name: str
    value: str
    inline: Optional[bool]


class EmbedDict(TypedDict):
    title: Any
    description: Any
    url: Optional[str]
    color: Optional[colors.Colorish]
    colour: Optional[colors.Colorish]
    timestamp: Optional[datetime.datetime]

    author: Optional[EmbedAuthor]
    footer: Optional[EmbedFooter]
    fields: Optional[Iterable[EmbedField]]
    thumbnail: Optional[files.Resourceish]
    image: Optional[files.Resourceish]
