#!/usr/bin/env python3
""" App Factory """
from flask import Flask, jsonify, redirect
from instance.config import app_config
from app.api.v2.models.database_models import DatabaseManager

# Custom error handlers
def page_not_found_error(err):
    """ 404 status custom return message """
    return jsonify({
        "status": 404,
        "error": "Resource not found on the server."
    }), 404

def method_not_not_allowed(err):
    """ 405 status custom return message """
    return jsonify({
        "status": 405,
        "error": "Method not allowed on this endpoint."
    }), 405

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
    """App factory """
    app = Flask(__name__, instance_relative_config=True)
    # config file loading
    app.config.from_object(app_config[config_mode])
    app.config.from_pyfile('config.py')
    # local imports
    from app.api.v1.views import party_views as parties_v1
    from app.api.v1.views import office_views as offices_v1
    from app.api.v2.views import party_views as parties_v2
    from app.api.v2.views import office_views as offices_v2
    from app.api.v2.views import users_views as users_v2
    from app.api.v2.views import candidate_views as candidates_v2
    # Register Blueprints
    app.register_blueprint(parties_v1.PARTY_BP_V1)
    app.register_blueprint(offices_v1.OFFICE_BP_V1)
    app.register_blueprint(parties_v2.PARTY_BP_V2)
    app.register_blueprint(offices_v2.OFFICE_BP_V2)
    app.register_blueprint(users_v2.AUTH_BP_V2)
    app.register_blueprint(candidates_v2.BASE_BP_V2)

    # Custom error handlers
    app.register_error_handler(404, page_not_found_error)
    app.register_error_handler(400, bad_user_request_error)
    app.register_error_handler(500, server_side_error)
    app.register_error_handler(405, method_not_not_allowed)

    # create database tables
    with app.app_context():
        db = DatabaseManager()
        db.create_all_tables()

    @app.route("/")
    def home():
        """ Home - Docs"""
        return redirect("https://documenter.getpostman.com/view/3796196/RztoKnTh#8203e67f-3ebe-4409-8e1b-85b0554d4773", code=302)

    return app


