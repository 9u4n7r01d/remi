import hikari
import lightbulb
from lightbulb import context
from sqlalchemy import select

from remi.db.schema import StaffRole
from remi.db.util import async_sql_session


@lightbulb.Check
async def is_moderator(ctx: context.Context) -> bool:
    author_id = ctx.author.id

    if author_id in await ctx.bot.fetch_owner_ids():
        return True

    if await is_administrator(ctx):
        return True

    with async_sql_session() as session:
        stmt = select(StaffRole.role_id).where(StaffRole.guild_id == ctx.guild_id).where(StaffRole.rank == "Moderator")
        query_result = (await session.execute(stmt)).scalars().all()

    return any([role in ctx.member.role_ids for role in query_result])


@lightbulb.Check
async def is_administrator(ctx: context.Context) -> bool:
    author_id = ctx.author.id

    if author_id in await ctx.bot.fetch_owner_ids():
        return True

    with async_sql_session() as session:
        stmt = (
            select(StaffRole.role_id).where(StaffRole.guild_id == ctx.guild_id).where(StaffRole.rank == "Administrator")
        )

        query_result = (await session.execute(stmt)).scalars().all()

    return any([role in ctx.member.role_ids for role in query_result])
