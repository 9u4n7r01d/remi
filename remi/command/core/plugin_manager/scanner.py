import importlib
import sys
from dataclasses import dataclass

import lightbulb

_CORE_COMMAND_PACKAGE = "remi.command.core"
_BUNDLED_COMMAND_PACKAGE = "remi.command.ext"


@dataclass(frozen=True)
class PluginInfo:
    load_path: str
    description: str


def _scan_plugin(plugin_package: str) -> dict[str, PluginInfo]:
    # Back up sys.modules, as importlib.import_module() will import the package and register to
    # sys.module, causing issues with lightbulb.bot.BotApp.load_extensions() and unload_extensions()
    old = sys.modules.copy()

    package = importlib.import_module(plugin_package)
    alias_mapping = {}

    for attr_str in dir(package):
        attr = getattr(package, attr_str)
        if not attr_str.startswith("__") and isinstance(attr, lightbulb.Plugin):
            alias_mapping[attr.name] = PluginInfo(
                load_path=f"{plugin_package}.{attr_str}", description=attr.description
            )

    # Restore the old sys.module
    sys.modules = old

    return alias_mapping


# noinspection PyDictCreation
def _get_all_plugin_info() -> dict[str, dict[str, PluginInfo]]:
    """Get all plugin currently available to the bot"""
    plugin_mapping = {}

    plugin_mapping["Core"] = _scan_plugin(_CORE_COMMAND_PACKAGE)
    plugin_mapping["Bundled"] = _scan_plugin(_BUNDLED_COMMAND_PACKAGE)

    return plugin_mapping
