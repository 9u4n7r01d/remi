import datetime
import logging
from typing import Optional

import hikari
from tzlocal import get_localzone

from remi.res.resource import Resource
from remi.util.typing import EmbedDict, EmbedField


def add_local_timezone(timestamp: datetime.datetime) -> datetime.datetime:
    """Get the local timezone to be added a datetime object"""
    return timestamp.replace(tzinfo=get_localzone())


def create_embed_from_dict(data: EmbedDict) -> hikari.Embed:
    """
    Create an embed without using post-init .set() methods. Creating an embed using this will
    manually tack in a local timezone with a small warning, instead of a giant wall of text
    from `hikari`
    :param EmbedDict data: The data needed to construct the embed
    :return: A `hikari.Embed` object
    """
    # Isolate fields that need their own initialization methods
    author = data.pop("author", None)
    footer = data.pop("footer", None)
    fields = data.pop("fields", None)
    thumbnail = data.pop("thumbnail", None)
    image = data.pop("image", None)

    # Final sanity check for timezone
    timestamp = data.pop("timestamp", None)
    if not timestamp:
        timestamp = datetime.datetime.now()
        logging.debug("Timestamp not found. Adding timestamp.")

    if not timestamp.tzinfo:
        timestamp = add_local_timezone(timestamp)
        logging.debug("No timezone data found. Applying local timezone.")

    # Create the embed
    embed = hikari.Embed(**data, timestamp=timestamp)

    if author:
        embed.set_author(**author)
    if footer:
        embed.set_footer(**footer)
    if thumbnail:
        embed.set_thumbnail(thumbnail)
    if image:
        embed.set_image(image)
    if fields:
        [embed.add_field(**field) for field in fields]

    return embed


def create_failure_embed(
    title: Optional[str] = None,
    description: Optional[str] = None,
    fields: Optional[list[EmbedField]] = None,
) -> hikari.Embed:
    """Generate a minimal failure embed"""
    template_embed = EmbedDict(
        title=title or "Something went wrong!",
        description=description or "Full traceback in terminal.",
        thumbnail=Resource.FAILURE_ICON,
        fields=fields,
        color=0xED254E,
    )
    return create_embed_from_dict(template_embed)


def create_success_embed(
    title: Optional[str] = None,
    description: Optional[str] = None,
    fields: Optional[list[EmbedField]] = None,
) -> hikari.Embed:
    """Generate a minimal success embed"""
    template_embed = EmbedDict(
        title=title or "Success",
        description=description,
        thumbnail=Resource.SUCCESS_ICON,
        fields=fields,
        color=0x71F79F,
    )
    return create_embed_from_dict(template_embed)
