import os
import sys


def resource_path(*parts: str) -> str:
    """Return an absolute path to a resource bundled with the app.

    Uses PyInstaller's _MEIPASS when available; otherwise resolves
    relative to the repository root.
    """
    # If running from a PyInstaller bundle
    base = getattr(sys, "_MEIPASS", None)
    if base is None:
        # repo root is parent of this utils package
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base, *parts)


def get_database_path(filename: str = "conversations.db") -> str:
    """Return the path to the application's database file.

    Defaults to `database/conversations.db` inside the project.
    """
    return resource_path("database", filename)
