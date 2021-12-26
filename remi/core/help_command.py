import hikari
import lightbulb
from lightbulb import commands, context, plugins
from lightbulb.help_command import filter_commands
from lightbulb.utils import ButtonNavigator, EmbedPaginator

from remi.res import Resource
from remi.util.embed import create_embed_from_dict


class HelpCommand(lightbulb.BaseHelpCommand):
    EMBED_PAG_MAX_LINE = 30
    EMBED_PAG_MAX_CHAR = 1024

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
        help_lines = list(unique_commands)
        help_lines.insert(0, f"__**{plugin.name}** - *{plugin.description}*__")
        help_lines.append("")

        return help_lines

    @staticmethod
    def _build_bot_help_embed(page_index: int, page_content: str) -> hikari.Embed:
        embed_dict = {
            "title": "**Available commands**",
            "description": page_content,
            "color": 0x7CB7FF,
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
        help_embed = EmbedPaginator(
            max_lines=self.EMBED_PAG_MAX_LINE, max_chars=self.EMBED_PAG_MAX_CHAR
        )
        help_embed.set_embed_factory(self._build_bot_help_embed)

        # Build the embed
        if not plugin:  # No plugin specified
            plugins_ = self.bot.plugins.values()
        else:
            plugins_ = [plugin]

        for plugin in plugins_:
            [help_embed.add_line(line) for line in await self._gather_command_helps(plugin, ctx)]

        navigator = ButtonNavigator(help_embed.build_pages())
        await navigator.run(ctx)

    async def send_plugin_help(self, ctx: context.base.Context, plugin: plugins.Plugin) -> None:
        await self.send_bot_help(ctx, plugin)
