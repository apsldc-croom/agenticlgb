"""
config/settings/local.py

Local developer overrides.
---------------------------------------------------
This file is .gitignore'd so each developer can
customize without affecting the team.

Copy .env.example to .env.dev and set your values,
or override settings directly here.
"""

from .dev import *  # noqa: F401, F403

# Override anything you need locally, for example:
# DATABASES["default"]["NAME"] = ROOT_DIR / "my_local.sqlite3"  # noqa: F405
