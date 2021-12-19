__name__ = "remi"
__version__ = "0.1.0"

import logging

from dotenv import load_dotenv
from rich.logging import RichHandler

load_dotenv()

# Set up logging
logging.basicConfig(
    format="%(message)s",
    handlers=[
        RichHandler(rich_tracebacks=True, show_time=True, log_time_format="%y/%m/%d %H:%M:%S")
    ],
)

logging.getLogger(__name__).addHandler(logging.NullHandler())
