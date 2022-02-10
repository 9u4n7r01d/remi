import hikari
import lightbulb
from rich import print as _rprint
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from remi.core.constant import Banner, Client
from remi.core.help_command import HelpCommand
from remi.db import Base

# Banner
_rprint(Banner.banner_text)

# Get our bot instance
bot = lightbulb.BotApp(
    token=Client.token,
    prefix=Client.prefix,
    banner=None,
    help_class=HelpCommand,
    owner_ids=Client.owner_ids,
)


# Set up some listener for events. In the future we might do some fancy async or DB that needs
# graceful construction and deconstruction, so it's better to have some scaffold in place beforehand
@bot.listen(hikari.StartingEvent)
async def on_starting(_) -> None:
    async_engine = bot.d.sql_engine = create_async_engine(
        f"sqlite+aiosqlite:///{Client.config_path}/config.sqlite", future=True
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot.d.sql_session = sessionmaker(
        async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=True,
    )


@bot.listen(hikari.StoppingEvent)
async def on_stopping(_) -> None:
    await bot.d.sql_engine.dispose()


@bot.listen(hikari.StartedEvent)
async def on_started(_) -> None:
    pass


# Load these by default
bot.load_extensions("remi.command.core.self")
bot.load_extensions("remi.command.core.plugin_manager")
bot.load_extensions("remi.command.core.about")
