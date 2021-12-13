import hikari
import logging
import datetime


def embed_from_dict(data: dict) -> hikari.Embed:
    """
    Construct a hikari.Embed object from a dictionary. This can be done by hikari.Embed(**kwargs),
    however, due to embed fields being added in separately, code will be repeated/-duplicated.

    TODO: Change this to use `dataclass` or similar instead of `dict` for type-checking

    For structure, refer to docs/embed_dict.md
    :param dict data: The `dict` to construct the embed.
    :return: A `hikari.Embed` object
    """
    # Isolate various fields that need its own method to set
    author = data.pop("author", None)
    footer = data.pop("footer", None)
    thumbnail = data.pop("thumbnail", None)
    image = data.pop("image", None)
    fields = data.pop("fields", None)

    # Safety net for timezones
    if not data["timestamp"].tzinfo:
        local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        logging.warning(
            "An embed without timezone (TZ) has been detected! Setting local TZ as embed's TZ."
        )
        data["timestamp"] = data["timestamp"].replace(tzinfo=local_timezone)

    # Construct the embed
    embed = hikari.Embed(**data)

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
