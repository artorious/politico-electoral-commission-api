#!/usr/bin/env python3
""" Runner"""
import os
from app import create_app


app = create_app("development")

if __name__ == "__main__":
    app.run()
