from functools import partial

import hikari
import lightbulb
from lightbulb import commands, context

from remi.core.constant import Global
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
@lightbulb.implements(*Global.group_implements)
async def plg_man(ctx: context.Context) -> None:
    pass


async def plg_man_handler(ctx: context.Context, operation: str):
    """Handler for all plugin-related operation"""
    target_plugins = ctx.options.plugins
    resp = create_success_embed(
        title=f"Successfully {operation.lower()}ed {len(target_plugins)} plugins",
        description="\n".join([f"\N{BULLET} `{plugin}`" for plugin in target_plugins]),
    )

    match operation:
        case "LOAD":
            plugin_manager.app.load_extensions(*target_plugins)

        case "UNLOAD":
            plugin_manager.app.unload_extensions(*target_plugins)

        case "RELOAD":
            plugin_manager.app.reload_extensions(*target_plugins)

    await ctx.respond(embed=resp)


_OPTION_KWARGS = {
    "name": "plugins",
    "type": str,
    "required": True,
    "modifier": commands.OptionModifier.GREEDY,
}


@plg_man.child
@lightbulb.option(description="The plugin(s)'s import path to load", **_OPTION_KWARGS)
@lightbulb.command(name="load", description="Load plugin(s).", inherit_checks=True)
@lightbulb.implements(*Global.sub_implements)
async def plg_man_load(ctx: context.Context) -> None:
    await plg_man_handler(ctx, "LOAD")


@plg_man.child
@lightbulb.option(description="The plugin(s)'s import path to unload", **_OPTION_KWARGS)
@lightbulb.command(name="unload", description="Unload plugin(s).", inherit_checks=True)
@lightbulb.implements(*Global.sub_implements)
async def plg_man_unload(ctx: context.Context) -> None:
    await plg_man_handler(ctx, "UNLOAD")


@plg_man.child
@lightbulb.option(description="The plugin(s)'s import path to reload", **_OPTION_KWARGS)
@lightbulb.command(name="reload", description="Reload plugin(s).", inherit_checks=True)
@lightbulb.implements(*Global.sub_implements)
async def plg_man_reload(ctx: context.Context) -> None:
    await plg_man_handler(ctx, "RELOAD")
