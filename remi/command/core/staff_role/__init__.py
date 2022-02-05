import lightbulb

from remi.core.constant import Client
from remi.core.exceptions import ProtectedPlugin

from .staff_role import staff_role_plugin

__plugin_name__ = "Staff Role"
__plugin_description__ = "Manage server's designated staff roles"


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(staff_role_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    if Client.dev_mode:
        bot.remove_plugin(staff_role_plugin)
    else:
        raise ProtectedPlugin(f"Cannot unload protected plugin `{staff_role_plugin.name}`!")
