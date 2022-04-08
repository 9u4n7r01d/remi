import asyncio

import lightbulb
from sqlalchemy import select

from remi.core.constant import Client
from remi.core.exceptions import ProtectedPlugin
from remi.db.engine import async_config_session
from remi.db.schema.config import ServerPrefix

from .prefix import prefix_manager

__plugin_name__ = prefix_manager.name
__plugin_description__ = prefix_manager.description


async def build_prefix_cache(bot: lightbulb.BotApp):
    async with async_config_session() as session:
        stmt = select((ServerPrefix.guild_id, ServerPrefix.prefix))
        prefix_mapping = dict((await session.execute(stmt)).all())
        bot.d.prefix_cache = prefix_mapping


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(prefix_manager)
    asyncio.run(build_prefix_cache(bot))


def unload(bot: lightbulb.BotApp) -> None:
    if Client.DEV_MODE:
        bot.remove_plugin(prefix_manager)
    else:
        raise ProtectedPlugin(f"Cannot unload protected plugin {prefix_manager.name}!")
