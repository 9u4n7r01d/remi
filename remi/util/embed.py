import datetime
import logging
from typing import Optional

import hikari
from tzlocal import get_localzone

from remi.res.resource import Resource
from remi.util.typing import EmbedDict, EmbedField


def _add_local_timezone(timestamp: datetime.datetime) -> datetime.datetime:
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
        logging.debug("Timestamp for embed not found. Adding timestamp.")

    if not timestamp.tzinfo:
        timestamp = _add_local_timezone(timestamp)
        logging.debug("No timezone data found in timestamp. Applying local timezone.")

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


def _generic_embed_handler(
    title: Optional[str], description: Optional[str], fields: Optional[list[EmbedField]], operation: str
):
    match operation:
        case "FAILURE":
            default_title = "Something went wrong!"
            thumbnail = Resource.FAILURE_ICON
            color = 0xED254E

        case "WARNING":
            default_title = "Warning!"
            thumbnail = Resource.WARNING_ICON
            color = 0xF9DC5C

        case "SUCCESS":
            default_title = "Success!"
            thumbnail = Resource.SUCCESS_ICON
            color = 0x71F79F

    # noinspection PyUnboundLocalVariable
    # As this is intended to be used only internally we don't care if default_title can be unbound
    template_embed_dict = EmbedDict(
        title=title or default_title,
        description=description,
        thumbnail=thumbnail,
        fields=fields,
        color=color,
    )
    return create_embed_from_dict(template_embed_dict)


def create_failure_embed(
    title: Optional[str] = None,
    description: Optional[str] = None,
    fields: Optional[list[EmbedField]] = None,
) -> hikari.Embed:
    """Generate a minimal failure embed"""
    return _generic_embed_handler(title=title, description=description, fields=fields, operation="FAILURE")


def create_success_embed(
    title: Optional[str] = None,
    description: Optional[str] = None,
    fields: Optional[list[EmbedField]] = None,
) -> hikari.Embed:
    """Generate a minimal success embed"""
    return _generic_embed_handler(title=title, description=description, fields=fields, operation="SUCCESS")


def create_warning_embed(
    title: Optional[str] = None,
    description: Optional[str] = None,
    fields: Optional[list[EmbedField]] = None,
) -> hikari.Embed:
    """Generate a minimal warning embed"""
    return _generic_embed_handler(title=title, description=description, fields=fields, operation="WARNING")
