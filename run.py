#!/usr.bin/env python3
""" Runner"""
import os
from app import create_app

config_mode = os.getenv("APP_SETTINGS")
app = create_app(config_mode)

if __name__ == "__main__":
    app.run()
