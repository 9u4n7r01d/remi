import hikari
import lightbulb
from lightbulb import commands, context
from remi.util.embed import EmbedDict, create_embed_from_dict
from remi.res.resource import Resource

# Plugin definition and boilerplate
core = lightbulb.Plugin("Core")
core.add_checks(lightbulb.checks.owner_only)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(core)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(core)


# Commands
@core.command
@lightbulb.command(name="ping", description="Ping the bot. Dirty way to ensure it's online.")
@lightbulb.implements(commands.SlashCommand, commands.PrefixCommand)
async def core_ping(ctx: context.Context):
    embed_response = EmbedDict(
        title="**Success!**",
        description="Bot is (hopefully) still alive!",
        thumbnail=Resource.SUCCESS_ICON,
        fields=[
            {"name": "Heartbeat latency", "value": f"{core.app.heartbeat_latency * 1000:.2f}ms"}
        ],
    )
    await ctx.respond(embed=create_embed_from_dict(embed_response))


@core.command
@lightbulb.command(name="shutdown", description="Shutdown the bot.")
@lightbulb.implements(commands.SlashCommand, commands.PrefixCommand)
async def core_shutdown(ctx: context.Context):
    await ctx.respond("Shutting down...")
    await core.bot.close()
