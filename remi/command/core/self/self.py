import hikari
import lightbulb
from lightbulb import context

from remi.core.constant import Global
from remi.util.embed import create_success_embed

self = lightbulb.Plugin("Self", description="Interact directly with Remi")


@self.command
@lightbulb.command(name="ping", description="Ping Remi. Dirty way to ensure she's online.")
@lightbulb.implements(*Global.COMMAND_IMPLEMENTS)
async def core_ping(ctx: context.Context):
    ping_result_embed = create_success_embed(
        title="**Success!**",
        description="Remi is (hopefully) still alive!",
        fields=[{"name": "Heartbeat latency", "value": f"{self.app.heartbeat_latency * 1000:.2f}ms"}],
    )
    await ctx.respond(embed=ping_result_embed)


@self.command
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command(name="shutdown", description="Shutdown Remi.")
@lightbulb.implements(*Global.COMMAND_IMPLEMENTS)
async def core_shutdown(ctx: context.Context):
    await ctx.respond("Shutting down...")
    await self.bot.close()
