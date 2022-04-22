__name__ = "remi"  # pylint: disable=redefined-builtin
__version__ = "0.0.3"

import logging as _logging
import os as _os
import sys as _sys
import warnings as _warnings

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
# Somehow, if chucked inside __init__, the usual click syntax fails Debugging shows that click exits
# due to standalone mode being True. So let's do some magic to get the context, and manual labor to
# exit if `--help`
@_click.command()
@_click.option("-v", "--verbose", help="Increase verbosity (can be stacked).", count=True)
@_click.option("-f", "--file", help="Enable writing log files (rotated at midnight).", is_flag=True)
@_click.option("--dev", help="Enable developer mode.", is_flag=True)
@_click.option("--log-sql", help="Enable logging of SQL.", is_flag=True)
@_click.pass_context
def cb_get_click_context(ctx, *args, **kwargs):  # Callback
    return ctx


_ctx = cb_get_click_context(standalone_mode=False)  # pylint: disable=no-value-for-parameter

if not _ctx:  # If we're calling with --help, get_context() will return 0
    _sys.exit(0)

# Set up logging
# Mapping for logging level
match _ctx.params["verbose"]:
    case 0:
        _LOGGING_LEVEL = 20  # INFO
        _LOGURU_LEVEL_PADDING = 8
    case 1:
        _LOGGING_LEVEL = 10  # DEBUG
        _LOGURU_LEVEL_PADDING = 8
    case 2:
        _LOGGING_LEVEL = 5  # TRACE_HIKARI
        _LOGURU_LEVEL_PADDING = 12
    case _:
        _LOGGING_LEVEL = 0  # NOTSET
        _LOGURU_LEVEL_PADDING = 12

# Remove the default handler and replace it with our customizable one
_logger.remove()

_log_format = (
    "<g>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | "
    f"<lvl>{{level: <{_LOGURU_LEVEL_PADDING}}}</> | "
    "<c>{name}</>:<c>{function}</>:<c>{line}</> - <lvl>{message}</>"
)

# Loguru handlers
_logger.add(_sys.stderr, format=_log_format, level=_LOGGING_LEVEL)


def warning_interceptor(message, *args, **kwargs):
    _logger.warning(f"{args[0].__name__} (from {args[1]}): {message}")


_warnings.showwarning = warning_interceptor

if _ctx.params["file"]:
    _logger.add("remi.log", rotation="00:00", format=_log_format, level=_LOGGING_LEVEL)

# Custom levels for loguru
_logger.level(name="TRACE_HIKARI", no=5, color="<m><b>")

# Start logging
_logging.basicConfig(handlers=[_InterceptHandler()], level=_LOGGING_LEVEL)

# Set up certain logging handler of interest as needed
if _ctx.params["log_sql"]:
    _logging.getLogger("sqlalchemy").setLevel(_LOGGING_LEVEL)

# Development mode-related configuration
if _ctx.params["dev"]:
    _os.environ["REMI_DEVMODE"] = "True"
