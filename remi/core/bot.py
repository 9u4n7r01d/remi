import hikari
import lightbulb
from remi.core.config import Config


# Get our bot instance
bot = lightbulb.BotApp(token=Config.token, prefix=Config.prefix)


# Set up some listener for events. In the future we might do some fancy async or DB that needs
# graceful construction and deconstruction, so it's better to have some scaffold in place beforehand
@bot.listen(hikari.StartingEvent)
async def on_starting() -> None:
    pass


@bot.listen(hikari.StoppingEvent)
async def on_stopping() -> None:
    pass


@bot.listen(hikari.StartedEvent)
async def on_started() -> None:
    pass
