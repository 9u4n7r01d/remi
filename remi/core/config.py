import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()


class Config:
    token: Final[str] = os.getenv("TOKEN")
