<div align="center">

<img src="https://cdn.discordapp.com/avatars/915949859679371285/b121cd5ce21e025c0c2e785703e50df7.png"><br>

# (Operator) Remi
A Discord bot built on `hikari` + `lightbulb` to manage my server<br>
</div>

## But why [`hikari`](https://github.com/hikari-py/hikari) + [`lightbulb`](https://github.com/tandemdude/hikari-lightbulb)?
I could have chosen [`Red-DiscordBot`](https://github.com/Cog-Creators/Red-DiscordBot) like my old projects (that never get to see the light of day). But, due to Red being bound to Python 3.9 because [`discord.py`](https://github.com/Rapptz/discord.py/), and I can't be arsed to make her cooperate with Python 3.10 ~~because one gotta ride the software update train~~, **and** because `discord.py` is dead, with [`pycord`](https://github.com/Pycord-Development/pycord) being its mere corpse reanimated sloppily. Might as well take the time to learn a new framework.

It's scary, yes; I have to reimplement some features I take for granted from `Red-DiscordBot`, yes. But I don't see why I need to stay in my comfortable zone. Plus, it's something I've been sitting on for quite a while, might as well take a stab at it.

As for why `lightbulb`, it's a coin flip.

## Instruction
### Installation
```shell
git clone https://github.com/PythonTryHard/remi
cd remi

# For normal usage
poetry install --no-dev

# For development
poetry install  
pre-commit install
```
### Setting up
In the repository root, edit `.env.example` then rename it to `.env`. Example:
```shell
TOKEN='Your token goes here'
BOT_PREFIX='op!'
OWNER_IDS=31415,92653,58979,32385
```
- `TOKEN`: Your bot's token, obtained from [Discord Developer Dashboard](https://discord.com/developers).
- `BOT_PREFIX`: Your preferred prefix for your bot.
- `OWNER_IDS`: Comma-separated Discord user IDs. Those assigned will have full access to the bot's functionality. Use with care.
### Usage
```
$ remi --help
Usage: remi [OPTIONS]

Options:
  -v, --verbose  Increase verbosity (can be stacked).
  -f, --file     Enable writing log files (rotated at midnight)
  --help         Show this message and exit.
```

## Contribution
All contributions are welcomed, whether issues, PRs, or even typo corrections.


## Attribution
- `/remi/res/*`: [Flaticon's UIcon](https://www.flaticon.com/uicons)
- [Profile picture](https://www.pixiv.net/en/artworks/74584596): Cropped from [RONOPU's](https://www.pixiv.net/en/users/13735243) artwork. I used to play King's Raid. Tempted to play it again.

## License
See [LICENSE](https://github.com/PythonTryHard/remi/blob/f5c42ae7c1263c5a9f889ad5b74ff61f0b8d0c12/LICENSE). TL; DR: MIT License
