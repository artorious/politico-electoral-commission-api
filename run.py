#!/usr.bin/env python3
""" Runner"""
from flask import Flask

app = Flask(__name__, instance_relative_config=True)

if __name__ == "__main__":
    app.run(DEBUG=True)
