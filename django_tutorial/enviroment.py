"""ENVIRONMENT."""

import os

ENVIRONMENT = os.getenv('ENVIRONMENT')
HOST = os.getenv('HOST')
SETTINGS_MODULE = 'config.settings.' + ENVIRONMENT
