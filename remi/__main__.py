from remi.core import bot

import click
import logging


@click.command()
@click.option("-v", "--verbose", help="Increase verbosity (can be stacked).", count=True)
def main(verbose: int) -> None:
    # Mapping for logging level
    match verbose:
        case 0:
            logging_level = "INFO"
        case 1:
            logging_level = "DEBUG"
        case _:
            logging_level = "NOTSET"

    # Set root logger's logging level
    logging.getLogger().setLevel(logging_level)

    bot.run()


main()
