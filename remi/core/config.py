import os
from typing import Final


class Config:
    token: Final[str] = os.getenv("TOKEN")
    prefix: Final[str] = os.getenv("BOT_PREFIX")
