import hikari
import lightbulb

from remi.core.constant import Global
from remi.core.help_command import HelpCommand

# Get our bot instance
bot = lightbulb.BotApp(
    token=Global.token,
    prefix=Global.prefix,
    banner=None,
    help_class=HelpCommand,
    owner_ids=Global.owner_ids,
)


# Set up some listener for events. In the future we might do some fancy async or DB that needs
# graceful construction and deconstruction, so it's better to have some scaffold in place beforehand
@bot.listen(hikari.StartingEvent)
async def on_starting(_) -> None:
    pass


@bot.listen(hikari.StoppingEvent)
async def on_stopping(_) -> None:
    pass


@bot.listen(hikari.StartedEvent)
async def on_started(_) -> None:
    pass


# Load these by default
bot.load_extensions("remi.command.core.core")
bot.load_extensions("remi.command.core.plugin_manager")
bot.load_extensions("remi.command.core.about")
