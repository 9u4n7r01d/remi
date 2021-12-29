import os
from typing import Final


class Config:
    token: Final[str] = os.getenv("TOKEN")
    prefix: Final[str] = os.getenv("BOT_PREFIX")
    owner_ids: Final[tuple[int]] = tuple(int(i) for i in os.getenv("OWNER_IDS").split(","))
