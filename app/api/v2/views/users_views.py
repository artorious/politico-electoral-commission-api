#!/usr/bin/env python3
""" Users Views """
from flask import Blueprint, jsonify, request
from app.api.v2.models.users_models import Users
from app.api.v2.models.database_models import DatabaseManager
from app.api.v2.models.validation_helper import ValidationHelper

AUTH_BP_V2 = Blueprint("v2_auth", __name__, url_prefix="/api/v2/auth")


@AUTH_BP_V2.route("/signup", methods=["POST"])
def create_user():
    """ Create a user account """
    custom_response = None
    user_reg_data = request.get_json(force=True)
    sample_user = Users(user_reg_data)

    if len(user_reg_data) > 8:
        custom_response = jsonify(sample_user.more_data_fields_response), 400

    elif len(user_reg_data) < 8:
        custom_response = jsonify(sample_user.few_data_fields_response), 400

    elif sample_user.validate_user_reg_data() is None:
        custom_response = jsonify(sample_user.create_user_account()), 201

    else:
        custom_response = sample_user.validate_user_reg_data()
    return custom_response
