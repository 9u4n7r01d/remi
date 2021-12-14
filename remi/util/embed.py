import hikari
import logging
import datetime
from tzlocal import get_localzone
from remi.util.embed_typing import EmbedDict


def add_local_timezone(timestamp: datetime.datetime) -> datetime.datetime:
    """Get the local timezone to be added a datetime object"""
    return timestamp.replace(tzinfo=get_localzone())


def create_embed_from_dict(data: EmbedDict, suppress_tz_warning=True) -> hikari.Embed:
    """
    Create an embed without using post-init .set() methods. Creating an embed using this will
    manually tack in a local timezone with a small warning, instead of a giant wall of text
    from `hikari`
    :param EmbedDict data: The data needed to construct the embed
    :param bool suppress_tz_warning: Prevent a logging.warning() call from this function
    :return: A `hikari.Embed` object
    """
    # Convert to a regular dict to keep PyCharm happy
    data_dict = dict(data)

    # Isolate fields that need their own initialization methods
    author = data_dict.pop("author", None)
    footer = data_dict.pop("footer", None)
    fields = data_dict.pop("fields", None)
    thumbnail = data_dict.pop("thumbnail", None)
    image = data_dict.pop("image", None)

    # Final sanity check for timezone
    if not data_dict["timestamp"].tzinfo:
        data_dict["timestamp"] = add_local_timezone(data_dict["timestamp"])

        if not suppress_tz_warning:
            logging.warning(
                "An embed with timestamp was constructed with timezone data. Applying local timezone."
            )

    # Create the embed
    embed = hikari.Embed(**data_dict)

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
