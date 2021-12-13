import os
import sys

import hikari
import lightbulb
from lightbulb import commands, context

from remi.core.config import Config


# Get our bot instance
bot = lightbulb.BotApp(token=Config.token, prefix="op!", banner=None)
