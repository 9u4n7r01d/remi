__name__ = "remi"
__version__ = "0.1.0"

import logging as _logging
import sys as _sys

import click as _click
from dotenv import load_dotenv
from loguru import logger as _logger

load_dotenv()


# Logging interceptor for directing logging to loguru.logger
class _InterceptHandler(_logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = _logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = _logging.currentframe(), 2
        while frame.f_code.co_filename == _logging.__file__:
            frame = frame.f_back
            depth += 1

        _logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# Voodoo magic from StackOverflow to make click work from __init__.py
#
# Somehow, if chucked inside __init__, the usual click syntax fails if defined and called here.
# Debugging shows that click exits due to standalone mode being True. So let's do some magic to get
# the context, and manual labor to exit if `--help`
@_click.command()
@_click.option("-v", "--verbose", help="Increase verbosity (can be stacked).", count=True)
@_click.pass_context
def get_click_context(ctx, *args, **kwargs):
    return ctx


_ctx = get_click_context(standalone_mode=False)

if not _ctx:  # If we're calling with --help, get_context() will return 0
    _sys.exit(0)

else:
    # Mapping for logging level
    match _ctx.params["verbose"]:
        case 0:
            _logging_level = 20  # INFO
            _loguru_level_padding = 8
        case 1:
            _logging_level = 10  # DEBUG
            _loguru_level_padding = 8
        case 2:
            _logging_level = 5  # TRACE_HIKARI
            _loguru_level_padding = 12
        case _:
            _logging_level = 0  # NOTSET
            _loguru_level_padding = 12

    # Remove the default handler and replace it with our customizable one
    _logger.remove()

    _log_format = (
        "<g>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | "
        f"<lvl>{{level: <{_loguru_level_padding}}}</> | "
        "<c>{name}</>:<c>{function}</>:<c>{line}</> - <lvl>{message}</>"
    )

    _logger.add(_sys.stderr, format=_log_format, level=_logging_level)

    # Custom levels for loguru
    _logger.level(name="TRACE_HIKARI", no=5, color="<m><b>")

    # Start logging
    _logging.basicConfig(handlers=[_InterceptHandler()], level=_logging_level)
