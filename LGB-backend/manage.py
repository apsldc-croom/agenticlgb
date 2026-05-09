#!/usr/bin/env python
"""
Django management entry point for the LGB platform.

Usage:
    python manage.py runserver
    python manage.py migrate
    python manage.py createsuperuser

Settings are resolved via DJANGO_SETTINGS_MODULE env var.
Default: config.settings.dev
"""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    # Add src/ to the Python path so Django can find config, pm, etc.
    src_dir = Path(__file__).resolve().parent / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "config.settings.dev",
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed "
            "and available on your PYTHONPATH environment variable? "
            "Did you forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
