import logging
import os
from typing import Final


def parse_owner_ids():
    try:
        return tuple(int(i) for i in os.getenv("OWNER_IDS").split(","))
    except (AttributeError, ValueError):
        logging.warning("Could not parse environment variable OWNER_IDS, using default owner(s)")
        return ()


class Config:
    token: Final[str] = os.getenv("TOKEN")
    prefix: Final[str] = os.getenv("BOT_PREFIX")
    owner_ids: Final[tuple[int]] = parse_owner_ids()
