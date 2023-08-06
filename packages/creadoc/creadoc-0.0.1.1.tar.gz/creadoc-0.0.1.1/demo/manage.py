#!/usr/bin/env python
# coding:utf-8
import os
import sys

project_path = os.path.dirname(__file__)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    execute_from_command_line(sys.argv)

