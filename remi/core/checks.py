import lightbulb
from hikari.permissions import Permissions
from lightbulb import checks, context
from sqlalchemy import select

from remi.db.schema.config import StaffRole
from remi.db.util import async_config_session


@lightbulb.Check
async def is_moderator(ctx: context.Context) -> bool:
    if await is_administrator(ctx):
        return True

    if checks.has_guild_permissions(Permissions.KICK_MEMBERS, Permissions.BAN_MEMBERS)(ctx):
        return True

    async with async_config_session() as session:
        stmt = select(StaffRole.role_id).where(StaffRole.guild_id == ctx.guild_id).where(StaffRole.rank == "Moderator")
        query_result = (await session.execute(stmt)).scalars().all()

    return any([role in ctx.member.role_ids for role in query_result])


@lightbulb.Check
async def is_administrator(ctx: context.Context) -> bool:
    author_id = ctx.member.id

    if author_id in await ctx.bot.fetch_owner_ids():
        return True

    if author_id == (await ctx.get_guild().fetch_owner()).id:
        return True

    if checks.has_guild_permissions(Permissions.MANAGE_GUILD, Permissions.ADMINISTRATOR)(ctx):
        return True

    async with async_config_session() as session:
        stmt = (
            select(StaffRole.role_id).where(StaffRole.guild_id == ctx.guild_id).where(StaffRole.rank == "Administrator")
        )

        query_result = (await session.execute(stmt)).scalars().all()

    return any([role in ctx.member.role_ids for role in query_result])
