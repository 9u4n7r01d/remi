import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Tuple

from lightbulb import commands


def parse_owner_ids():
    try:
        return tuple(int(i) for i in os.getenv("OWNER_IDS").split(","))
    except (AttributeError, ValueError):
        logging.warning("Could not parse environment variable OWNER_IDS, using default owner(s)")
        return ()


@dataclass(frozen=True)
class Global:
    command_implements: Final = (commands.SlashCommand, commands.PrefixCommand)
    group_implements: Final = (commands.SlashCommandGroup, commands.PrefixCommandGroup)
    sub_implements: Final = (commands.SlashSubCommand, commands.PrefixSubCommand)


@dataclass(frozen=True)
class Client:
    token: Final[str] = os.getenv("TOKEN")
    prefix: Final[str] = os.getenv("BOT_PREFIX")
    owner_ids: Final[Tuple[int]] = parse_owner_ids()
