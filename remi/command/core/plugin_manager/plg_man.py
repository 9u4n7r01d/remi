from functools import partial

import hikari
import lightbulb
from lightbulb import commands, context

from remi.core.constant import Global
from remi.core.exceptions import ProtectedPlugin
from remi.util.embed import (
    create_embed_from_dict,
    create_failure_embed,
    create_success_embed,
)

from .scanner import _get_all_plugin_info, _get_all_plugin_name_mapping

# Plugin definition and boilerplate
plugin_manager = lightbulb.Plugin("Plugin Manager", description="Manage Remi's plugins")
plugin_manager.add_checks(lightbulb.checks.owner_only)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin_manager)


def unload(bot: lightbulb.BotApp) -> None:
    raise ProtectedPlugin(f"Cannot unload protected plugin {plg_man.name}!")


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

        case ProtectedPlugin():
            resp = failure_template(description="This plugin is critical to the bot's operation!")

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
    target_plugin = ctx.options.plugin

    if target_plugin not in (mapping := _get_all_plugin_name_mapping()):
        raise lightbulb.ExtensionNotFound(f"No extension by the name {target_plugin!r} was found.")
    else:
        load_path = mapping[target_plugin]

    match operation:
        case "LOAD":
            plugin_manager.app.load_extensions(load_path)

        case "UNLOAD":
            plugin_manager.app.unload_extensions(load_path)

        case "RELOAD":
            plugin_manager.app.reload_extensions(load_path)

    resp = create_success_embed(
        title=f"Successfully {operation.lower()}ed plugins `{target_plugin}`",
    )
    await ctx.respond(embed=resp)


_OPTION_KWARGS = {
    "name": "plugin",
    "type": str,
    "required": True,
    "modifier": commands.OptionModifier.CONSUME_REST,
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


@plg_man.child
@lightbulb.command(
    name="list", description="List available plugins and status.", inherit_checks=True
)
@lightbulb.implements(*Global.sub_implements)
async def plg_man_list(ctx: context.Context) -> None:
    plugin_mapping_all = _get_all_plugin_info()

    # Build plugin listing and status for each plugin category
    embed_text = []
    for category, mapping in plugin_mapping_all.items():
        listing_template = "`[{status}]` **{name}** - {description}"

        category_listing = []
        for plugin_name, info_object in mapping.items():
            category_listing.append(
                listing_template.format(
                    status="x" if info_object.load_path in ctx.bot.extensions else " ",
                    name=plugin_name,
                    description=info_object.description,
                )
            )

        embed_text.append(f"**{category}**\n" + "\n".join(category_listing))

    resp_embed = create_embed_from_dict(
        {
            "title": "Available plugins",
            "description": "\n".join(embed_text),
            "footer": {"text": "[x] means loaded, otherwise [ ]"},
            "color": 0x7CB7FF,
        }
    )

    await ctx.respond(embed=resp_embed)
