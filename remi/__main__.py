import os

from remi.core.bot import bot

if os.name != "nt":
    import uvloop

    uvloop.install()


def main():
    bot.run()


if __name__ == "__main__":
    main()
