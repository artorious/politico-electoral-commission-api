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


@AUTH_BP_V2.route("/login", methods=["POST"])
def login():
    """ User login """
    custom_response = None
    user_login_data = request.get_json(force=True)

    if len(user_login_data) > 2:
        custom_response = jsonify(
            ValidationHelper.more_data_fields_response), 400

    elif len(user_login_data) < 2:
        custom_response = jsonify(
            ValidationHelper.few_data_fields_response), 400

    elif ValidationHelper().check_for_expected_keys_in_user_input(
            user_login_data, ["email", "password"]) is False:
        custom_response = jsonify(
            ValidationHelper.unexpected_data_types_resp), 400
    raw_email = user_login_data["email"]
    raw_password = user_login_data["password"]

    if DatabaseManager().\
        lookup_whether_entity_exists_in_a_table_by_attrib(
            "users", "email", raw_email) and DatabaseManager().\
            verify_user_password(raw_password, raw_email):
        uid = DatabaseManager().fetch_entity_id(
            "uid", "users", "email", raw_email)
        auth_token = Users.generate_token(uid)
        DatabaseManager().update_login_timestamp(raw_email)
        custom_response = jsonify({
            "status": 200,
            "message": [{
                "token": auth_token.decode('utf-8'),
                "user": f'{raw_email} Logged in Successfuly'}]}), 200
    else:
        custom_response = jsonify({
            "status": 401,
            "error": "Invalid email or password, Please try again"}), 401

    return custom_response
