#!/usr/bin/env python
"""
Script to run Django development server on public host (0.0.0.0)
This allows the server to be accessible from other devices on the network.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omantel.settings")
    django.setup()
    
    # Run server on 0.0.0.0:8000 to allow public access
    # You can change the port by modifying the last argument
    sys.argv = ["manage.py", "runserver", "0.0.0.0:8000"]
    execute_from_command_line(sys.argv)
