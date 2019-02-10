#!/usr/bin/env python3
""" Runner"""
import os
from app import create_app

# config_mode = os.getenv("APP_SETTINGS")
# app = create_app(config_mode)
app = create_app("development")

if __name__ == "__main__":
    app.run()
