from typing import Iterable, Union

import hikari
import lightbulb
import sqlalchemy.ext.asyncio
from lightbulb import commands, context
from lightbulb.converters.special import RoleConverter
from sqlalchemy import delete, select

from remi.core.checks import is_administrator
from remi.core.constant import Global
from remi.db.schema import StaffRole
from remi.db.util import async_sql_session
from remi.util.embed import (
    create_failure_embed,
    create_info_embed,
    create_success_embed,
    create_warning_embed,
)
from remi.util.typing import EmbedDict, EmbedField

staff_role_plugin = lightbulb.Plugin("Staff Role", description="Manage server's designated staff roles")
staff_role_plugin.add_checks(is_administrator)


@staff_role_plugin.command
@lightbulb.command(name="staff", description="Manage this server's staff roles.")
@lightbulb.implements(*Global.group_implements)
async def staff_command(ctx: context.Context):
    pass


def _parse_rank(rank_arg: str) -> Union[str, None]:
    match rank_arg.lower():
        case "moderator" | "mod":
            rank = "Moderator"
        case "administrator" | "admin":
            rank = "Administrator"
        case _:
            rank = None
    return rank


async def _is_in_db(rank: str, *role_ids: int) -> Iterable[int]:
    session: sqlalchemy.ext.asyncio.AsyncSession
    async with async_sql_session() as session:
        stmt = select(StaffRole.role_id).where(StaffRole.role_id.in_(role_ids)).where(StaffRole.rank == rank)
        result = (await session.execute(stmt)).scalars().all()

    return result


def _handler_docstring(remove):
    docstring = f"""
    This command can operate on **multiple roles at once**.

    __**Arguments' constraints**__
    For __`rank`__, only 2 options are allowed (**case-insensitive**, can be shortened):
        \N{BULLET} `"Administrator"` (`"Admin"`).
        \N{BULLET} `"Moderator"` (`"Mod"`).

    For __`rank`__, it must be either:
        \N{BULLET} A valid rank mention (`@Moderator`).
        \N{BULLET} A valid rank ID (`314159265358979`).

    __**Example usage**__
        \N{BULLET} `[p]staff {"set" if not remove else "remove"} mod 314159265358979`
        \N{BULLET} `[p]staff {"set" if not remove else "remove"} admin @Administrator`
        \N{BULLET} `[p]staff {"set" if not remove else "remove"} mod 31415 92653 58979 32385`
    """
    return docstring


async def staff_edit_handler(ctx: context.Context, remove=False):
    if not (rank := _parse_rank(ctx.options.rank)):
        await ctx.respond(embed=create_failure_embed(title=f"Unknown rank {ctx.options.rank!r}!"))
        return

    operation_result = []
    async with async_sql_session() as session:
        role_to_skip = await _is_in_db(rank, *[role.id for role in ctx.options.roles])
        if remove:
            role_to_skip = set(ctx.options.roles) - set(role_to_skip)  # Get roles NOT present in DB

        dupe_warning = False
        role: hikari.Role
        for role in ctx.options.roles:
            if (role_id := role.id) in role_to_skip:
                dupe_warning = True
                if remove:
                    operation_result.append(f"\N{WARNING SIGN} {role.mention} is not `{rank}`")
                else:
                    operation_result.append(f"\N{WARNING SIGN} {role.mention} is already `{rank}`")

            else:
                entry = StaffRole(server_id=ctx.guild_id, rank=rank, role_id=role_id)
                if remove:
                    operation_result.append(f"\N{WHITE HEAVY CHECK MARK} {role.mention} removed from `{rank}`")
                    await session.delete(entry)
                else:
                    operation_result.append(f"\N{WHITE HEAVY CHECK MARK} {role.mention} added as `{rank}`")
                    session.add(entry)

        else:
            await session.commit()

    role_set_embed = EmbedDict(title="Result", description="\n".join(operation_result))

    if dupe_warning:
        role_set_embed = create_warning_embed(**role_set_embed)
    else:
        role_set_embed = create_success_embed(**role_set_embed)

    await ctx.respond(embed=role_set_embed)


@staff_command.child
@lightbulb.set_help(text=_handler_docstring(remove=False))
@lightbulb.option(
    name="roles",
    description="The role(s) of interest.",
    type=hikari.Role,
    modifier=commands.OptionModifier.GREEDY,
    required=True,
)
@lightbulb.option(name="rank", description="The equivalent rank to set rank(s) to.", required=True)
@lightbulb.command(name="set", description="Set a role to be equivalent to moderator/administrator.")
@lightbulb.implements(*Global.sub_implements)
async def staff_set(ctx: context.Context):
    await staff_edit_handler(ctx, remove=False)


@staff_command.child
@lightbulb.set_help(text=_handler_docstring(remove=True))
@lightbulb.option(
    name="roles",
    description="The role(s) of interest.",
    type=hikari.Role,
    modifier=commands.OptionModifier.GREEDY,
    required=True,
)
@lightbulb.option(name="rank", description="The equivalent rank to set rank(s) to.", required=True)
@lightbulb.command(name="remove", description="Remove a role from being equivalent to moderator/administrator.")
@lightbulb.implements(*Global.sub_implements)
async def staff_remove(ctx: context.Context):
    await staff_edit_handler(ctx, remove=True)


async def _query_role(ctx: context.Context, stmt: sqlalchemy.sql.Selectable) -> Iterable[str]:
    async with async_sql_session() as session:
        result = (await session.execute(stmt)).scalars().all()
    return [(await RoleConverter(ctx).convert(str(role_id))).mention for role_id in result]


@staff_command.child
@lightbulb.command(name="info", description="List out current server's rank settings.")
@lightbulb.implements(*Global.sub_implements)
async def staff_list(ctx: context.Context):
    base_stmt = select(StaffRole.role_id).where(StaffRole.guild_id == ctx.guild_id)
    select_moderator = base_stmt.where(StaffRole.rank == "Moderator")
    select_administrator = base_stmt.where(StaffRole.rank == "Administrator")

    role_info_embed = create_info_embed(
        title=f"Staff role info for `{ctx.get_guild().name}`",
        fields=[
            EmbedField(
                name="Moderator",
                value="\n".join([f"\N{BULLET} {role}" for role in await _query_role(ctx, select_moderator)]) or "None",
                inline=True,
            ),
            EmbedField(
                name="Administrator",
                value="\n".join([f"\N{BULLET} {role}" for role in await _query_role(ctx, select_administrator)])
                or "None",
                inline=True,
            ),
        ],
    )

    await ctx.respond(embed=role_info_embed)


@staff_command.child
@lightbulb.command(name="reset", description="Reset server's staff.")
@lightbulb.implements(*Global.sub_implements)
async def staff_reset(ctx: context.Context):
    stmt = delete(StaffRole).where(StaffRole.guild_id == ctx.guild_id)

    async with async_sql_session() as session:
        await session.execute(stmt)

    await ctx.respond(embed=create_success_embed(title="Staff roles has been reset for this server!"))
