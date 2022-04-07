import lightbulb

from remi.core.constant import Client
from remi.core.exceptions import ProtectedPlugin

from .about import about

__plugin_name__ = about.name
__plugin_description__ = about.description


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(about)


def unload(bot: lightbulb.BotApp) -> None:
    if Client.DEV_MODE:
        bot.remove_plugin(about)
    else:
        raise ProtectedPlugin(f"Cannot unload protected plugin {about.name}!")
