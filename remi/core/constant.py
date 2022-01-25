import logging
import os
from dataclasses import dataclass
from pathlib import Path
from sys import exit
from typing import Final, Tuple

from lightbulb import commands


def parse_owner_ids():
    try:
        return tuple(int(i) for i in os.getenv("OWNER_IDS").split(","))
    except (AttributeError, ValueError):
        logging.warning("Could not parse environment variable OWNER_IDS, using default owner(s)")
        return ()


def parse_config_path() -> Path:
    if not (config_path_env_var := os.getenv("CONFIG_PATH")):
        config_path = Path(".")
        logging.warning(f"`CONFIG_PATH` not set. Defaulting to current directory.")
    else:
        config_path = Path(config_path_env_var)

    if not config_path.is_absolute():
        config_path = config_path.absolute()
        print(f"Do you want to use '{config_path}' to store config folder? (y/N): ", end="")

        match input().lower():
            case "y":
                logging.info(f"Using '{config_path}' as config folder")
                logging.info(f"To suppress this message, set `CONFIG_PATH` to '{config_path}'")
            case _:
                exit(1)

    if not config_path.exists():
        logging.info(f"Attempting to create {config_path!r}...")
        try:
            config_path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            logging.error(f"Insufficient permission to create {config_path!r}. Exiting...")
            exit(1)

    return config_path


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
    config_path: Final[Path] = parse_config_path()
