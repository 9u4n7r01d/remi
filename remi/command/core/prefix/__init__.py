import lightbulb

from remi.core.constant import Client
from remi.core.exceptions import ProtectedPlugin

from .prefix import prefix_manager

__plugin_name__ = prefix_manager.name
__plugin_description__ = prefix_manager.description


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(prefix_manager)


def unload(bot: lightbulb.BotApp) -> None:
    if Client.dev_mode:
        bot.remove_plugin(prefix_manager)
    else:
        raise ProtectedPlugin(f"Cannot unload protected plugin {prefix_manager.name}!")
