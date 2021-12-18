import hikari
import lightbulb
from lightbulb import commands, context
from remi.util.embed import create_success_embed, create_failure_embed
from functools import partial


# Plugin definition and boilerplate
ext_manager_plugin = lightbulb.Plugin("Cog")
ext_manager_plugin.add_checks(lightbulb.checks.owner_only)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ext_manager_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext_manager_plugin)


# Error handler
@ext_manager_plugin.set_error_handler
async def on_cog_command_error(event: lightbulb.CommandErrorEvent) -> bool:
    # Unpack the exception since we're going do it anyway
    exception = event.exception or event.exception.__cause__

    # Prime up a failure embed template
    failure_template = partial(create_failure_embed, title=exception.args[0])

    match exception:
        case lightbulb.ExtensionNotFound():
            resp = failure_template(description="Please double check input.")

        case lightbulb.ExtensionAlreadyLoaded():
            resp = failure_template(description="Extension is already loaded.")

        case lightbulb.ExtensionNotLoaded():
            resp = failure_template(description="Extension is not loaded.")

        case lightbulb.ExtensionMissingLoad():
            resp = failure_template(description="Ensure load() is present in the extension.")

        case lightbulb.ExtensionMissingUnload():
            resp = failure_template(description="Ensure unload() is present in the extension.")

        # Default case for everything not handled.
        case _:
            resp = create_failure_embed(
                f"Unhandled `{type(exception).__name__}` raised in `{__name__}`!"
            )
            await event.context.respond(embed=resp)
            return False

    await event.context.respond(embed=resp)
    return True


# Commands
@ext_manager_plugin.command
@lightbulb.command(name="ext", description="Manage hot-(un)loading of extensions.")
@lightbulb.implements(commands.SlashCommandGroup, commands.PrefixCommandGroup)
async def core_extman(ctx: context.Context) -> None:
    pass


@core_extman.child
@lightbulb.option(
    name="cogs",
    description="The extension's import path to load",
    type=str,
    required=True,
    modifier=commands.OptionModifier.GREEDY,
)
@lightbulb.command(name="load", description="Load extension(s).")
@lightbulb.implements(commands.SlashSubCommand, commands.PrefixSubCommand)
async def core_extman_load(ctx: context.Context) -> None:
    for cog in ctx.options.cogs:
        ext_manager_plugin.app.load_extensions(cog)

    resp = create_success_embed(
        title=f"Successfully loaded {len(ctx.options.cogs)} extensions",
        description="\n".join([f"`+ {cog}`" for cog in ctx.options.cogs]),
    )

    await ctx.respond(embed=resp)


@core_extman.child
@lightbulb.option(
    name="cogs",
    description="The extension's import path to load",
    type=str,
    required=True,
    modifier=commands.OptionModifier.GREEDY,
)
@lightbulb.command(name="unload", description="Unload extension(s).")
@lightbulb.implements(commands.SlashSubCommand, commands.PrefixSubCommand)
async def core_extman_load(ctx: context.Context) -> None:
    for cog in ctx.options.cogs:
        ext_manager_plugin.app.unload_extensions(cog)

    resp = create_success_embed(
        title=f"Successfully unloaded {len(ctx.options.cogs)} extensions",
        description="\n".join([f"`+ {cog}`" for cog in ctx.options.cogs]),
    )

    await ctx.respond(embed=resp)


@core_extman.child
@lightbulb.option(
    name="cogs",
    description="The extension's import path to load",
    type=str,
    required=True,
    modifier=commands.OptionModifier.GREEDY,
)
@lightbulb.command(name="reload", description="Reload extension(s).")
@lightbulb.implements(commands.SlashSubCommand, commands.PrefixSubCommand)
async def core_extman_load(ctx: context.Context) -> None:
    for cog in ctx.options.cogs:
        ext_manager_plugin.app.reload_extensions(cog)

    resp = create_success_embed(
        title=f"Successfully reloaded {len(ctx.options.cogs)} extensions",
        description="\n".join([f"`+ {cog}`" for cog in ctx.options.cogs]),
    )

    await ctx.respond(embed=resp)
