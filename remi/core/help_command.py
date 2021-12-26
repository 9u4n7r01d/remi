import hikari
import lightbulb
from lightbulb import commands, context, plugins
from lightbulb.help_command import filter_commands
from lightbulb.utils import ButtonNavigator, EmbedPaginator

from remi.res import Resource
from remi.util.embed import create_embed_from_dict


class HelpCommand(lightbulb.BaseHelpCommand):
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
        # Prepare the embed
        help_embed = EmbedPaginator(max_lines=30, max_chars=1024)
        help_embed.set_embed_factory(self._build_bot_help_embed)

        # Build the embed
        for name, plugin in self.bot.plugins.items():
            help_embed.add_line(f"__**{name}** - *{plugin.description}*__")
            [help_embed.add_line(line) for line in await self._gather_commands(plugin, ctx)]
            help_embed.add_line("")

        navigator = ButtonNavigator(help_embed.build_pages())
        await navigator.run(ctx)
