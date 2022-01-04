import hikari
import lightbulb
from lightbulb import commands, context

from remi.core.constant import Global
from remi.core.exceptions import ProtectedPlugin
from remi.util.embed import create_success_embed

# Plugin definition and boilerplate
core = lightbulb.Plugin("Core", description="Remi's core commands")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(core)


def unload(bot: lightbulb.BotApp) -> None:
    raise ProtectedPlugin(f"Cannot unload protected plugin `{core.name}`!")


# Commands
@core.command
@lightbulb.command(name="ping", description="Ping the bot. Dirty way to ensure it's online.")
@lightbulb.implements(*Global.implements)
async def core_ping(ctx: context.Context):
    embed_response = create_success_embed(
        title="**Success!**",
        description="Bot is (hopefully) still alive!",
        fields=[
            {"name": "Heartbeat latency", "value": f"{core.app.heartbeat_latency * 1000:.2f}ms"}
        ],
    )
    await ctx.respond(embed=embed_response)


@core.command
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command(name="shutdown", description="Shutdown the bot.")
@lightbulb.implements(*Global.implements)
async def core_shutdown(ctx: context.Context):
    await ctx.respond("Shutting down...")
    await core.bot.close()
