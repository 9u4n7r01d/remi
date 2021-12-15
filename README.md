<div align="center">

<img src="https://cdn.discordapp.com/avatars/915949859679371285/b121cd5ce21e025c0c2e785703e50df7.png"><br>

# (Operator) Remi
A Discord bot built on `hikari` + `lightbulb` to manage my server<br>
</div>

## But why [`hikari`](https://github.com/hikari-py/hikari) + [`lightbulb`](https://github.com/tandemdude/hikari-lightbulb)?
I could have chosen [`Red-DiscordBot`](https://github.com/Cog-Creators/Red-DiscordBot) like my old projects (that never get to see the light of day). But, due to Red being bound to Python 3.9 because [`discord.py`](https://github.com/Rapptz/discord.py/), and I can't be arsed to make her cooperate with Python 3.10 ~~because one gotta ride the software update train~~, **and** because `discord.py` is dead, with [`pycord`](https://github.com/Pycord-Development/pycord) being its mere corpse reanimated sloppily. Might as well take the time to learn a new framework.

It's scary, yes; I have to reimplement some features I take for granted from `Red-DiscordBot`, yes. But I don't see why I need to stay in my comfortable zone. Plus, it's something I've been sitting on for quite a while, might as well take a stab at it.

As for why `lightbulb`, it's a coin flip.

## Development
This repo uses [`pre-commit`](https://github.com/pre-commit/pre-commit) and [`poetry`](https://github.com/python-poetry/poetry), and Python `3.10.x` for workflow, and `black` for code style.

### Reminder that...
- Lint your code before you commit! `pre-commit` should handle this already, but just in case!
- If you're abstracting something complex, do write tests to ensure it doesn't subtly mess things up and/or fail.

### Instruction

1. Clone the repository
```bash
git clone https://github.com/PythonTryHard/remi
```

2. Install all dependencies and pre-commit hooks
```bash
cd remi
poetry shell
poetry install
pre-commit install
```

3. Specify a `.env` file with the following data
```bash
TOKEN=''   # Your bot's token goes here
PREFIX=''  # Your bot's prefix goes here
```

4. Run with
```bash
python -m remi
```
at repository's root since this repo utilizes some relative path magic that will subtly fail.

## Attribution
- `/remi/res/*`: [Flaticon's UIcon](https://www.flaticon.com/uicons)
- [Profile picture](https://www.pixiv.net/en/artworks/74584596): Cropped from [RONOPU's](https://www.pixiv.net/en/users/13735243) artwork. I used to play King's Raid. Tempted to play it again.

## License
See [LICENSE](https://github.com/PythonTryHard/remi/blob/f5c42ae7c1263c5a9f889ad5b74ff61f0b8d0c12/LICENSE). TL; DR: MIT License
