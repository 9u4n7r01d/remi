"""
All classes are marked total=False so checkers won't raise warnings for incomplete initialization,
because these are ultimately for type hinting around a wrapper for hikari.Embed() and its various
.set() methods that supply their own default values for keys marked with Optional types.
"""

import datetime
from typing import Any, Iterable, Optional, TypedDict

from hikari import colors, files


class EmbedAuthor(TypedDict, total=False):
    name: Optional[str]
    url: Optional[str]
    icon: Optional[files.Resourceish]


class EmbedFooter(TypedDict, total=False):
    text: Optional[str]
    icon: Optional[files.Resourceish]


class EmbedField(TypedDict, total=False):
    name: str
    value: str
    inline: Optional[bool]


class EmbedDict(TypedDict, total=False):
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
