import typing
from collections import defaultdict

import hikari
import lightbulb
from lightbulb import commands, context, plugins
from lightbulb.help_command import filter_commands
from lightbulb.utils import ButtonNavigator, EmbedPaginator

from remi.res import Resource
from remi.util.embed import create_embed_from_dict


class HelpCommand(lightbulb.BaseHelpCommand):
    @staticmethod
    def _sort_dict(target: dict):
        return {k: v for k, v in sorted(target.items(), key=lambda ele: ele[0])}

    @staticmethod
    async def _gather_commands(plugin: plugins.Plugin, ctx: context.Context):
        """Recursively gather all unique commands of a cog and description"""
        unique_commands = set()

        for cmd in await filter_commands(plugin.all_commands, ctx):
            match cmd:
                case lightbulb.PrefixCommandGroup() | lightbulb.SlashCommandGroup():
                    help_line = f"**`{cmd.name}`** - (Group) {cmd.description}"
                case _:
                    help_line = f"**`{cmd.name}`** - {cmd.description}"

            unique_commands.add(help_line)

        return unique_commands

    @staticmethod
    def _build_bot_help_embed(page_index: int, page_content: str):
        embed_dict = {
            "title": "**Available commands**",
            "description": page_content,
            "color": 0x7CB7FF,
            "footer": {"text": "Auto-generated"},
            "thumbnail": Resource.HELP_ICON,
        }
        return create_embed_from_dict(embed_dict)

    async def send_bot_help(self, ctx: context.Context) -> None:
        """Default help message when `[p]help` is called without arguments"""
        # Gather extensions' information
        plugin_dict = defaultdict(dict)
        for name, plugin in self.bot.plugins.items():
            plugin_dict[name]["description"] = plugin.description
            plugin_dict[name]["commands"] = await self._gather_commands(plugin, ctx)

        # Prepare the embed
        help_embed = EmbedPaginator(max_lines=30, max_chars=1024)
        help_embed.set_embed_factory(self._build_bot_help_embed)

        for name in plugin_dict:
            help_embed.add_line(f"__**{name}** - *{plugin_dict[name]['description']}*__")
            [help_embed.add_line(line) for line in plugin_dict[name]["commands"]]
            help_embed.add_line("")

        navigator = ButtonNavigator(help_embed.build_pages())
        await navigator.run(ctx)
