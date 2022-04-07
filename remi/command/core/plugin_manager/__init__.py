import lightbulb

from remi.core.constant import Client
from remi.core.exceptions import ProtectedPlugin

from .plg_man import plugin_manager

__plugin_name__ = plugin_manager.name
__plugin_description__ = plugin_manager.description


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin_manager)


def unload(bot: lightbulb.BotApp) -> None:
    if Client.DEV_MODE:
        bot.remove_plugin(plugin_manager)
    else:
        raise ProtectedPlugin(f"Cannot unload protected plugin {plugin_manager.name}!")
