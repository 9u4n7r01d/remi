import lightbulb

from remi.core.constant import Client
from remi.core.exceptions import ProtectedPlugin

from .self import self

__plugin_name__ = self.name
__plugin_description__ = self.description


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(self)


def unload(bot: lightbulb.BotApp) -> None:
    if Client.dev_mode:
        bot.remove_plugin(self)
    else:
        raise ProtectedPlugin(f"Cannot unload protected plugin `{self.name}`!")
