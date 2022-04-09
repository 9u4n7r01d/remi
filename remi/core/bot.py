import hikari
import lightbulb
from rich import print as _rprint

from remi.core.constant import Banner, Client
from remi.core.help_command import HelpCommand
from remi.db.engine import async_config_engine, dispose_all_engines
from remi.db.schema.config import ConfigBase

# Banner
_rprint(Banner.banner_text)


# Prefix getter
async def get_prefix(app: lightbulb.BotApp, message: hikari.Message) -> list[str]:
    return app.d.prefix_cache.get(message.guild_id, Client.PREFIX)


# Get our bot instance
bot = lightbulb.BotApp(
    token=Client.TOKEN,
    prefix=lightbulb.app.when_mentioned_or(get_prefix),
    banner=None,
    help_class=HelpCommand,
    owner_ids=Client.OWNER_IDS,
)


# Set up some listener for events. In the future we might do some fancy async or DB that needs
# graceful construction and deconstruction, so it's better to have some scaffold in place beforehand
@bot.listen(hikari.StartingEvent)
async def on_starting(_) -> None:
    async with async_config_engine.begin() as conn:
        await conn.run_sync(ConfigBase.metadata.create_all)


@bot.listen(hikari.StoppingEvent)
async def on_stopping(_) -> None:
    await dispose_all_engines()


@bot.listen(hikari.StartedEvent)
async def on_started(_) -> None:
    pass


# Load these by default
bot.load_extensions("remi.command.core.self")
bot.load_extensions("remi.command.core.plugin_manager")
bot.load_extensions("remi.command.core.about")
bot.load_extensions("remi.command.core.staff_role")
bot.load_extensions("remi.command.core.prefix")
