import datetime
import string
from random import choices, randint, uniform

import hikari
import pytest

from remi.util.embed import EmbedDict, add_local_timezone, create_embed_from_dict

START_OF_TIME = -62135536000.0  # datetime.datetime(1,1,2,0,0,0)
END_OF_TIME = 253402189199.0  # datetime.datetime(9999,12,30,23,59,59)
URL = "https://example.org"
IMAGE = "1x1.png"


def randstr(a, b):
    """Generate random string of length a <= len <= b"""
    return "".join(choices(string.printable, k=randint(a, b)))


def randbool():
    """Generate random bool"""
    return randint(0, 1) == 1


def embed_test(include_timezone):
    """Test if embed_from_dict() is generating embeds correctly"""
    # Generate kwargs-able embed parameter with random data
    title, description, url = [randstr(10, 50) for _ in range(3)]
    color = randint(0x000000, 0xFFFFFF)
    timestamp = datetime.datetime.fromtimestamp(uniform(START_OF_TIME, END_OF_TIME))

    # We run two tests: with timezone data and without
    if include_timezone:
        timestamp = add_local_timezone(timestamp)

    # Create the embed and dictionary to prepare for fields
    embed_explicit = hikari.Embed(
        title=title, description=description, url=url, color=color, timestamp=timestamp
    )
    data_dict = {
        "title": title,
        "description": description,
        "url": url,
        "color": color,
        "timestamp": timestamp,
    }

    # Randomly generate the author
    author_name = randstr(10, 50)
    author_url = URL
    author_icon = IMAGE

    embed_explicit.set_author(name=author_name, url=author_url, icon=author_icon)
    data_dict["author"] = {"name": author_name, "url": author_url, "icon": author_icon}

    # Randomly generate the footer
    footer_text = randstr(10, 50)
    footer_icon = IMAGE

    embed_explicit.set_footer(text=footer_text, icon=footer_icon)
    data_dict["footer"] = {"text": footer_text, "icon": footer_icon}

    # Randomly generate the thumbnail and image
    embed_explicit.set_thumbnail(IMAGE)
    data_dict["thumbnail"] = IMAGE

    embed_explicit.set_image(IMAGE)
    data_dict["image"] = IMAGE

    # Randomly generate the fields
    for _ in range(randint(0, 50)):
        field_name = randstr(10, 50)
        field_value = randstr(10, 50)
        field_inline = randbool()

        embed_explicit.add_field(name=field_name, value=field_value, inline=field_inline)

        if "fields" not in data_dict.keys():
            data_dict["fields"] = []  # Work-around for tests

        data_dict["fields"].append(
            {"name": field_name, "value": field_value, "inline": field_inline}
        )

    # Generate the embed automatically to compare
    embed_implicit = create_embed_from_dict(EmbedDict(**data_dict))

    assert embed_implicit == embed_explicit


@pytest.mark.repeat(5)
def test_with_tz():
    embed_test(include_timezone=True)


@pytest.mark.repeat(5)
@pytest.mark.filterwarnings("ignore")
def test_without_tz():
    # This test is going to throw warnings about timezone. Let's not have it spill onto the terminal
    embed_test(include_timezone=False)
