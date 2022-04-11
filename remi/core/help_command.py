# pylint: disable=arguments-renamed
from typing import Union

import hikari
import lightbulb
from lightbulb import commands, context, plugins
from lightbulb.help_command import filter_commands
from lightbulb.utils import ButtonNavigator, EmbedPaginator

from remi.res import Resource
from remi.util.embed import create_embed_from_dict

LightbulbCommandGroup = Union[
    commands.PrefixCommandGroup,
    commands.PrefixSubGroup,
    commands.SlashCommandGroup,
    commands.SlashSubGroup,
]


class HelpCommand(lightbulb.BaseHelpCommand):
    EMBED_PAG_MAX_LINE = 30
    EMBED_PAG_MAX_CHAR = 1024
    EMBED_COLOR = 0x7CB7FF

    @staticmethod
    async def _gather_command_helps(plugin: plugins.Plugin, ctx: context.Context) -> list[str]:
        """Generate help for `[p]help` and `[p]help plugin`"""
        # Get all unique commands and generate their help
        unique_commands = set()

        for cmd in await filter_commands(plugin.all_commands, ctx):
            match cmd:
                case lightbulb.PrefixCommandGroup() | lightbulb.SlashCommandGroup():
                    help_line = f"**`{cmd.name}`** - (Group) {cmd.description}"
                case _:
                    help_line = f"**`{cmd.name}`** - {cmd.description}"

            unique_commands.add(help_line)

        # Prepare the help lines for EmbedPaginator.add_line()
        help_lines = sorted(unique_commands)
        help_lines.insert(0, f"__**{plugin.name}** - *{plugin.description}*__")
        help_lines.append("")

        if not unique_commands:  # Author has no access to all commands of plugin
            help_lines.insert(1, "None")

        return help_lines

    def _build_bot_help_embed(self, page_index: int, page_content: str) -> hikari.Embed:
        embed_dict = {
            "title": "**Available commands**",
            "description": page_content,
            "color": self.EMBED_COLOR,
            "footer": {"text": "Auto-generated"},
            "thumbnail": Resource.HELP_ICON,
        }
        return create_embed_from_dict(embed_dict)

    async def send_bot_help(self, ctx: context.Context, plugin: plugins.Plugin = None) -> None:
        """
        Default help message when `[p]help` is called without arguments

        Doubles as `[p]help plugin` when `plugin` is supplied
        """
        # Prepare the embed
        help_embed = EmbedPaginator(max_lines=self.EMBED_PAG_MAX_LINE, max_chars=self.EMBED_PAG_MAX_CHAR)
        help_embed.set_embed_factory(self._build_bot_help_embed)

        # Build the embed
        if not plugin:  # No plugin specified
            plugins_ = self.bot.plugins.values()
        else:
            plugins_ = [plugin]

        for plg in sorted(plugins_, key=lambda x: x.name):
            [help_embed.add_line(line) for line in await self._gather_command_helps(plg, ctx)]

        navigator = ButtonNavigator(help_embed.build_pages())
        await navigator.run(ctx)

    async def send_plugin_help(self, ctx: context.base.Context, plugin: plugins.Plugin) -> None:
        await self.send_bot_help(ctx, plugin)

    async def send_command_help(self, ctx: context.Context, command: commands.Command) -> None:
        # Do not send help if author does not have sufficient permissions
        if not await filter_commands([command], ctx):
            return

        help_embed = create_embed_from_dict(
            {
                "title": f"Help for `{command.qualname}`",
                "description": f"*{command.description}*",
                "color": self.EMBED_COLOR,
                "footer": {"text": "Auto-generated, `[p]` is your bot's prefix"},
                "thumbnail": Resource.HELP_ICON,
                "fields": [
                    {
                        "name": "__Syntax__",
                        "value": f"`{command.signature}`",
                        "inline": True,
                    },
                    {
                        "name": "__Arguments__",
                        "value": "\n".join(
                            [f"\N{BULLET} `{name}` - {opt.description}" for name, opt in command.options.items()]
                        ),
                    },
                    {
                        "name": "__Note__",
                        "value": f"{command.get_help(ctx) or '*None*'}",
                    },
                ],
            }
        )

        await ctx.respond(embed=help_embed)

    # noinspection PyTypeChecker
    @staticmethod
    async def _gather_group_help(group: LightbulbCommandGroup, ctx: context.Context, level=0):
        """Recursively gather a group's command"""
        lines = []
        for cmd in await filter_commands(group.subcommands.values(), ctx):
            match cmd:
                case commands.PrefixSubCommand() | commands.SlashSubCommand():
                    lines.append(f"{'  ' * level}\N{BULLET} `{cmd.name}` - {cmd.description}")
                case commands.PrefixCommandGroup() | commands.SlashSubGroup():
                    await HelpCommand._gather_group_help(cmd, ctx, level=level + 1)

        return lines

    async def send_group_help(self, ctx: context.Context, group: LightbulbCommandGroup) -> None:
        # Do not send help if author does not have sufficient permissions
        if not await filter_commands([group], ctx):
            return

        help_embed = create_embed_from_dict(
            {
                "title": f"Help for command group `{group.name}`",
                "description": f"*{group.description}*",
                "color": self.EMBED_COLOR,
                "footer": {"text": "Auto-generated"},
                "thumbnail": Resource.HELP_ICON,
                "fields": [
                    {
                        "name": "All subcommands",
                        "value": "\n".join(await self._gather_group_help(group, ctx)),
                    }
                ],
            }
        )

        await ctx.respond(embed=help_embed)
