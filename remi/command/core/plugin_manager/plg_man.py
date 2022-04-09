import sys
from functools import partial
from importlib import reload

import lightbulb
from lightbulb import commands, context

from remi.core.constant import Global
from remi.core.exceptions import ProtectedPlugin
from remi.util.embed import (
    EmbedDict,
    create_embed_from_dict,
    create_failure_embed,
    create_success_embed,
)

from .plg_scan import _get_all_plugin_info, _get_all_plugin_name_mapping

plugin_manager = lightbulb.Plugin("Plugin Manager", description="Manage Remi's plugins.")
plugin_manager.add_checks(lightbulb.checks.owner_only)


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
                title=f"Unhandled `{type(exception).__name__}` raised in `{__name__}`!",
                description="Check terminal/log for full traceback.",
            )
            await event.context.respond(embed=resp)
            return False

    await event.context.respond(embed=resp)
    return True


@plugin_manager.command
@lightbulb.command(name="plugin", description="Manage hot-(un)loading of plugins.")
@lightbulb.implements(*Global.GROUP_IMPLEMENTS)
async def plg_man(ctx: context.Context) -> None:
    pass


async def plg_man_handler(ctx: context.Context, operation: str):
    """Handler for all plugin-related operation"""
    target_plugin = ctx.options.plugin

    if target_plugin not in (mapping := _get_all_plugin_name_mapping()):
        raise lightbulb.ExtensionNotFound(f"No extension by the name {target_plugin!r} was found.")

    load_path = mapping[target_plugin]

    reload_target = [i for i in sys.modules if load_path in i]

    match operation:
        case "LOAD":
            plugin_manager.app.load_extensions(load_path)

        case "UNLOAD":
            [reload(sys.modules[i]) for i in reload_target]
            plugin_manager.app.unload_extensions(load_path)

        case "RELOAD":
            [reload(sys.modules[i]) for i in reload_target]
            plugin_manager.app.unload_extensions(load_path)
            plugin_manager.app.load_extensions(load_path)

    load_status_embed = create_success_embed(
        title=f"Successfully {operation.lower()}ed plugins `{target_plugin}`",
    )
    await ctx.respond(embed=load_status_embed)


@plg_man.child
@lightbulb.option(
    name="plugin",
    description="The name of the plugin to load.",
    type=str,
    required=True,
    modifier=commands.OptionModifier.CONSUME_REST,
)
@lightbulb.command(name="load", description="Load a plugin.")
@lightbulb.implements(*Global.SUB_COMMAND_IMPLEMENTS)
async def plg_man_load(ctx: context.Context) -> None:
    await plg_man_handler(ctx, "LOAD")


@plg_man.child
@lightbulb.option(
    name="plugin",
    description="The name of the plugin to load.",
    type=str,
    required=True,
    modifier=commands.OptionModifier.CONSUME_REST,
)
@lightbulb.command(name="unload", description="Unload a plugin.")
@lightbulb.implements(*Global.SUB_COMMAND_IMPLEMENTS)
async def plg_man_unload(ctx: context.Context) -> None:
    await plg_man_handler(ctx, "UNLOAD")


@plg_man.child
@lightbulb.option(
    name="plugin",
    description="The name of the plugin to load.",
    type=str,
    required=True,
    modifier=commands.OptionModifier.CONSUME_REST,
)
@lightbulb.command(name="reload", description="Reload a plugin.")
@lightbulb.implements(*Global.SUB_COMMAND_IMPLEMENTS)
async def plg_man_reload(ctx: context.Context) -> None:
    await plg_man_handler(ctx, "RELOAD")


@plg_man.child
@lightbulb.command(name="list", description="List available plugins and status.")
@lightbulb.implements(*Global.SUB_COMMAND_IMPLEMENTS)
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
        EmbedDict(
            title="Available plugins",
            description="\n".join(embed_text),
            footer={"text": "[x] means loaded, otherwise [ ]"},
            color=0x7CB7FF,
        )
    )

    await ctx.respond(embed=resp_embed)
