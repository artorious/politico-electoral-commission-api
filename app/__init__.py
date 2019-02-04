#!/usr/bin/env python3
""" App Factory """
from flask import Flask
from instance.config import app_config


def create_app(config_mode):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_mode])
    app.config.from_pyfile('config.py')
    from app.api.v1 import party_views
    app.register_blueprint(party_views.BASE_BP_V1)
    return app


