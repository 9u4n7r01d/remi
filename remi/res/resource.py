from importlib import resources


class Resource:
    SUCCESS_ICON = resources.path("remi.res.png", "success.png")
    FAILURE_ICON = resources.path("remi.res.png", "failure.png")
    HELP_ICON = resources.path("remi.res.png", "help.png")
