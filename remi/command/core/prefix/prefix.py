import logging

import hikari
import lightbulb
from lightbulb import commands, context
from sqlalchemy import delete, select

import remi.core.checks
from remi.core.constant import Global
from remi.db.engine import async_config_session
from remi.db.schema.config import ServerPrefix
from remi.db.util import _unique_insert
from remi.util.embed import create_success_embed

prefix_manager = lightbulb.Plugin("Prefix Manager", description="Manage this server's prefix.")
prefix_manager.add_checks(lightbulb.checks.guild_only, remi.core.checks.is_administrator)


@prefix_manager.listener(hikari.StartingEvent)
async def build_prefix_cache(_: hikari.StartingEvent):
    logging.info("Building prefix cache...")
    async with async_config_session() as session:
        stmt = select((ServerPrefix.guild_id, ServerPrefix.prefix))
        prefix_mapping = dict((await session.execute(stmt)).all())
        prefix_manager.app.d.prefix_cache = prefix_mapping


@prefix_manager.command
@lightbulb.set_help(docstring=True)
@lightbulb.option(
    name="prefix",
    description="The prefix to use for this server (max. 5 characters).",
    modifier=commands.OptionModifier.CONSUME_REST,
)
@lightbulb.command(name="setprefix", description="Set a custom prefix for this server.")
@lightbulb.implements(*Global.COMMAND_IMPLEMENTS)
async def prefixman_setprefix(ctx: context.Context):
    """
    \N{BULLET} If supplied prefix is long than 5, the first 5 characters will be used.
    \N{BULLET} Any space character will be removed
    """
    clamped_length = min(5, max(0, len(ctx.options.prefix)))
    prefix = ctx.options.prefix[:clamped_length].replace(" ", "")

    entry = ServerPrefix(guild_id=ctx.guild_id, prefix=prefix)

    async with async_config_session() as session:
        await _unique_insert(entry, session)
        await session.commit()

        ctx.bot.d.prefix_cache[ctx.guild_id] = prefix

    await ctx.respond(embed=create_success_embed(title=f"Prefix for your server has been set to `{prefix}`!"))


@prefix_manager.command
@lightbulb.command(name="unsetprefix", description="Remove custom prefix for this server.")
@lightbulb.implements(*Global.COMMAND_IMPLEMENTS)
async def prefixman_unsetprefix(ctx: context.Context):
    async with async_config_session() as session:
        stmt = delete(ServerPrefix).where(ServerPrefix.guild_id == ctx.guild_id)

        await session.execute(stmt)
        await session.commit()

        try:
            del ctx.bot.d.prefix_cache[ctx.guild_id]
        except KeyError:
            pass

    await ctx.respond(embed=create_success_embed(title="Prefix for your server has been unset!"))
