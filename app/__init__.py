#!/usr/bin/env python3
""" App Factory """
from flask import Flask, jsonify
from instance.config import app_config

# Custom error handlers
def page_not_found_error(err):
    """ 404 status custom return message """
    return jsonify({
        "status": 404,
        "error": "Resource not found on the server."
    }), 404

def bad_user_request_error(err):
    """ 400 status custom return message """
    return jsonify({
        "status": 400,
        "error": "Malformed request syntax or invalid request message framing"
    }), 400

def server_side_error(err):
    """ 500 status custom return message """
    return jsonify({
        "status": 500,
        "error": "Internal Server Error. Unexpected condition"
    }), 500


def create_app(config_mode):
    app = Flask(__name__, instance_relative_config=True)
    # config file loading
    app.config.from_object(app_config[config_mode])
    app.config.from_pyfile('config.py')
    # local imports
    from app.api.v1 import party_views
    # Register Blueprints
    app.register_blueprint(party_views.BASE_BP_V1)
    # Custom error handlers
    app.register_error_handler(404, page_not_found_error)
    app.register_error_handler(400, bad_user_request_error)
    app.register_error_handler(500, server_side_error)
    return app


