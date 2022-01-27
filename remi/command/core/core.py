import hikari
import lightbulb
from lightbulb import commands, context

from remi.core.constant import Client, Global
from remi.core.exceptions import ProtectedPlugin
from remi.util.embed import create_success_embed

core = lightbulb.Plugin("Core", description="Remi's core commands.")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(core)


def unload(bot: lightbulb.BotApp) -> None:
    if Client.dev_mode:
        bot.remove_plugin(core)
    else:
        raise ProtectedPlugin(f"Cannot unload protected plugin `{core.name}`!")


@core.command
@lightbulb.command(name="ping", description="Ping the bot. Dirty way to ensure it's online.")
@lightbulb.implements(*Global.command_implements)
async def core_ping(ctx: context.Context):
    ping_result_embed = create_success_embed(
        title="**Success!**",
        description="Bot is (hopefully) still alive!",
        fields=[{"name": "Heartbeat latency", "value": f"{core.app.heartbeat_latency * 1000:.2f}ms"}],
    )
    await ctx.respond(embed=ping_result_embed)


@core.command
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command(name="shutdown", description="Shutdown the bot.")
@lightbulb.implements(*Global.command_implements)
async def core_shutdown(ctx: context.Context):
    await ctx.respond("Shutting down...")
    await core.bot.close()
