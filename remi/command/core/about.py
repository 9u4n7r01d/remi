import sys

import hikari
import lightbulb
import loguru
from lightbulb import commands, context

from remi.core.constant import Global
from remi.core.exceptions import ProtectedPlugin
from remi.util.embed import create_embed_from_dict

about = lightbulb.Plugin("About", description="Information about Remi")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(about)


def unload(bot: lightbulb.BotApp) -> None:
    raise ProtectedPlugin(f"Cannot unload protected plugin {about.name}!")


def _get_owner(ctx: context.Context):
    if team := ctx.bot.application.team:
        return f"Team {team.name}"
    else:
        return str(ctx.bot.application.owner)


@about.command
@lightbulb.command(name="about", description="About the bot.")
@lightbulb.implements(*Global.command_implements)
async def core_about(ctx: context.Context):
    owner = _get_owner(ctx)
    author = "https://github.com/PythonTryHard"
    remi_repo = author + "/remi"

    red_repo = "https://github.com/Cog-Creators/Red-DiscordBot"

    info = create_embed_from_dict(
        {
            "color": 0xF9DC5C,
            "fields": [
                {"name": "Instance's owner", "value": owner, "inline": True},
                {
                    "name": "Built on",
                    "value": "\n".join(
                        [
                            f"\N{BULLET} {i.__name__} v{i.__version__}"
                            for i in (hikari, lightbulb, loguru)
                        ]
                    ),
                    "inline": True,
                },
                {"name": "Python version", "value": f"{sys.version}"},
                {
                    "name": "About the bot",
                    "value": (
                        f"This bot is an instance of [`remi`]({remi_repo}), an open-source bot"
                        f"made by [PythonTryHard]({author}), taking inspiration from "
                        f"[`Red-DiscordBot`]({red_repo}), without which, I'd still be afraid to "
                        "design a proper Discord bot from the ground up.\n\n"
                        "To you, thank you for using `remi`. If there's any problem, please open an"
                        " issue on GitHub and I'll try to respond as quickly as possible.\n"
                        "PythonTryHard"
                    ),
                },
            ],
            "footer": {"text": f"Made with <3"},
            "thumbnail": ctx.bot.get_me().avatar_url,
        }
    )
    await ctx.respond(embed=info)
