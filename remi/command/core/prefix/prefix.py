import hikari
import lightbulb
from lightbulb import commands, context
from sqlalchemy import delete

import remi.core.checks
from remi.core.constant import Global
from remi.db.schema import ServerPrefix
from remi.db.util import async_sql_session
from remi.util.embed import create_success_embed

prefix_manager = lightbulb.Plugin("Prefix Manager", description="Manage this server's prefix.")
prefix_manager.add_checks(lightbulb.checks.guild_only, remi.core.checks.is_administrator)


@prefix_manager.command
@lightbulb.set_help(docstring=True)
@lightbulb.option(
    name="prefix",
    description="The prefix to use for this server (max. 5 characters).",
    modifier=commands.OptionModifier.CONSUME_REST,
)
@lightbulb.command(name="setprefix", description="Set a custom prefix for this server.", inherit_checks=True)
@lightbulb.implements(*Global.command_implements)
async def prefixman_setprefix(ctx: context.Context):
    """
    \N{BULLET} If supplied prefix is long than 5, the first 5 characters will be used.
    \N{BULLET} Any space character will be removed
    """
    clamped_length = min(5, max(0, len(ctx.options.prefix)))
    prefix = ctx.options.prefix[:clamped_length].replace(" ", "")

    async with async_sql_session() as session:
        entry = ServerPrefix(guild_id=ctx.guild_id, prefix=prefix)

        session.add(entry)
        await session.commit()

    await ctx.respond(embed=create_success_embed(title=f"Prefix for your server has been set to `{prefix}`!"))


@prefix_manager.command
@lightbulb.command(name="unsetprefix", description="Remove custom prefix for this server.", inherit_checks=True)
@lightbulb.implements(*Global.command_implements)
async def prefixman_unsetprefix(ctx: context.Context):
    async with async_sql_session() as session:
        stmt = delete(ServerPrefix).where(ServerPrefix.guild_id == ctx.guild_id)

        await session.execute(stmt)
        await session.commit()

    await ctx.respond(embed=create_success_embed(title=f"Prefix for your server has been reset!"))
