# pylint: disable=logging-fstring-interpolation, invalid-name
import logging
import os
import string
import sys
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from platform import machine, python_version, release, system
from typing import Final, Tuple

import hikari
import lightbulb
import loguru
import sqlalchemy
from lightbulb import commands


def parse_owner_ids():
    try:
        return tuple(int(i) for i in os.getenv("OWNER_IDS").split(","))
    except (AttributeError, ValueError):
        logging.warning("Could not parse environment variable OWNER_IDS, using default owner(s)")
        return ()


def get_data_path() -> Path:
    # Check for CONFIG_PATH's existence, default to current directory
    if not (data_path_env_var := os.getenv("DATA_PATH")):
        data_path = Path(".")
        logging.warning("`CONFIG_PATH` not set. Defaulting to current directory.")
    else:
        data_path = Path(data_path_env_var)

    # Convert CONFIG_PATH to absolute path
    if not data_path.is_absolute():
        data_path = data_path.absolute()
        print(f"Do you want to use '{data_path}' to store bot's data? (y/N): ", end="")

        match input().lower():
            case "y":
                logging.info(f"Using '{data_path}' as data folder.")
                logging.info(f"To suppress this message, set `DATA_PATH` to '{data_path}'.")
            case _:
                sys.exit(1)

    # Create CONFIG_PATH
    if not data_path.exists():
        logging.info(f"Attempting to create {data_path!r}...")
        try:
            data_path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            logging.error(f"Insufficient permission to create {data_path!r}. Exiting...")
            sys.exit(1)

    return data_path


def is_dev_mode() -> bool:
    return bool(os.getenv("REMI_DEVMODE", default=""))


@dataclass(frozen=True)
class Global:
    COMMAND_IMPLEMENTS: Final = (commands.SlashCommand, commands.PrefixCommand)
    GROUP_IMPLEMENTS: Final = (commands.SlashCommandGroup, commands.PrefixCommandGroup)
    SUB_COMMAND_IMPLEMENTS: Final = (commands.SlashSubCommand, commands.PrefixSubCommand)
    SUB_GROUP_IMPLEMENTS: Final = (commands.SlashSubGroup, commands.PrefixSubGroup)


@dataclass(frozen=True)
class Client:
    TOKEN: Final[str] = os.getenv("TOKEN")
    PREFIX: Final[str] = os.getenv("BOT_PREFIX")
    OWNER_IDS: Final[Tuple[int]] = parse_owner_ids()
    DATA_PATH: Final[Path] = get_data_path()
    DEV_MODE: Final[bool] = is_dev_mode()


class Banner:
    banner_text = string.Template(resources.read_text("remi.core", "banner.txt")).safe_substitute(
        hikari_version=hikari.__version__,
        lightbulb_version=lightbulb.__version__,
        loguru_version=loguru.__version__,
        sqlalchemy_version=sqlalchemy.__version__,
        system_info=f"{machine()} - {system()} {release()}",
        python_version=python_version(),
    )
