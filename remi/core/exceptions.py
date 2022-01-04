from lightbulb import LightbulbError


class ProtectedPlugin(LightbulbError):
    """Raise when user try to unload operation-critical plugins."""
