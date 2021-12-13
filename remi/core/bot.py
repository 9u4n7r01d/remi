import lightbulb

from remi.core.config import Config


# Get our bot instance
bot = lightbulb.BotApp(token=Config.token, prefix="op!", banner=None)
