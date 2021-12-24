from functools import partial

import hikari
import lightbulb
from lightbulb import commands, context

from remi.util.embed import create_failure_embed, create_success_embed

# Plugin definition and boilerplate
plugin_manager = lightbulb.Plugin("Plugin Manager", description="Manage Remi's plugins")
plugin_manager.add_checks(lightbulb.checks.owner_only)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin_manager)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin_manager)


# Error handler
@plugin_manager.set_error_handler
async def on_cog_command_error(event: lightbulb.CommandErrorEvent) -> bool:
    # Unpack the exception since we're going do it anyway
    exception = event.exception or event.exception.__cause__

    # Prime up a failure embed template
    failure_template = partial(create_failure_embed, title=exception.args[0])

    match exception:
        case lightbulb.ExtensionNotFound():
            resp = failure_template(description="Please double check input.")

        case lightbulb.ExtensionAlreadyLoaded():
            resp = failure_template(description="Plugin is already loaded.")

        case lightbulb.ExtensionNotLoaded():
            resp = failure_template(description="Plugin is not loaded.")

        case lightbulb.ExtensionMissingLoad():
            resp = failure_template(description="Ensure load() is present in the plugin.")

        case lightbulb.ExtensionMissingUnload():
            resp = failure_template(description="Ensure unload() is present in the plugin.")

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
@plugin_manager.command
@lightbulb.command(name="plugin", description="Manage hot-(un)loading of plugins.")
@lightbulb.implements(commands.SlashCommandGroup, commands.PrefixCommandGroup)
async def plg_man(ctx: context.Context) -> None:
    pass


@plg_man.child
@lightbulb.option(
    name="plugins",
    description="The plugin(s)'s import path to load",
    type=str,
    required=True,
    modifier=commands.OptionModifier.GREEDY,
)
@lightbulb.command(name="load", description="Load plugin(s).")
@lightbulb.implements(commands.SlashSubCommand, commands.PrefixSubCommand)
async def plg_man_load(ctx: context.Context) -> None:
    for cog in ctx.options.cogs:
        plugin_manager.app.load_extensions(cog)

    resp = create_success_embed(
        title=f"Successfully loaded {len(ctx.options.cogs)} plugin(s)",
        description="\n".join([f"`+ {cog}`" for cog in ctx.options.cogs]),
    )

    await ctx.respond(embed=resp)


@plg_man.child
@lightbulb.option(
    name="plugins",
    description="The plugin(s)'s import path to load",
    type=str,
    required=True,
    modifier=commands.OptionModifier.GREEDY,
)
@lightbulb.command(name="unload", description="Unload plugin(s).")
@lightbulb.implements(commands.SlashSubCommand, commands.PrefixSubCommand)
async def plg_man_unload(ctx: context.Context) -> None:
    for cog in ctx.options.cogs:
        plugin_manager.app.unload_extensions(cog)

    resp = create_success_embed(
        title=f"Successfully unloaded {len(ctx.options.cogs)} plugin(s)",
        description="\n".join([f"`+ {cog}`" for cog in ctx.options.cogs]),
    )

    await ctx.respond(embed=resp)


@plg_man.child
@lightbulb.option(
    name="plugins",
    description="The plugin(s)'s import path to load",
    type=str,
    required=True,
    modifier=commands.OptionModifier.GREEDY,
)
@lightbulb.command(name="reload", description="Reload plugin(s).")
@lightbulb.implements(commands.SlashSubCommand, commands.PrefixSubCommand)
async def plg_man_reload(ctx: context.Context) -> None:
    for cog in ctx.options.cogs:
        plugin_manager.app.reload_extensions(cog)

    resp = create_success_embed(
        title=f"Successfully reloaded {len(ctx.options.cogs)} plugin(s)",
        description="\n".join([f"`+ {cog}`" for cog in ctx.options.cogs]),
    )

    await ctx.respond(embed=resp)
