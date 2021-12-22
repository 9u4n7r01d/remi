import os

from remi.core import bot

if os.sys != "nt":
    import uvloop

    uvloop.install()


def main():
    bot.run()


main()
