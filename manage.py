#!/usr/bin/env python
import os
import sys
default_django_settings_module = "weathermonitor.settings.dev"


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", default_django_settings_module )

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
