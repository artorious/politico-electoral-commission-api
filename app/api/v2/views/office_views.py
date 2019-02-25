#!/usr/bin/env python3
""" Routes Office Information """

from flask import Blueprint, jsonify, request
from app.api.v2.models.office_models import PoliticalOffices
from app.api.v2.models.database_models import DatabaseManager
from app.api.v2.models.validation_helper import ValidationHelper

OFFICE_BP_V2 = Blueprint("v2_office", __name__, url_prefix="/api/v2/offices")


@OFFICE_BP_V2.route("", methods=["GET"])
def fetch_all_offices():
    """ Fetch all political offices (GET) """

    auth_header = request.headers.get('Authorization')
    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)

        if not isinstance(decoded_token, str):
            raw_offices = \
                DatabaseManager().fetch_all_records_in_a_table("offices")

            if raw_offices == []:
                custom_response = jsonify({
                    "data": "The Office list is empty", "status": 200
                }), 200
            else:
                data = []
                for record in raw_offices:
                    sample = {}
                    sample["Office ID"] = record["office_id"]
                    sample["Office Name"] = record["name"]
                    sample["Office Type"] = record["type"]
                    sample["Registration Timestamp"] = \
                        record["registration_timestamp"]
                    data.append(sample)
                custom_response = jsonify({
                    "status": 200, "Political Offices": data
                }), 200
        else:
            custom_response = jsonify({'message': decoded_token}), 401

    else:
        custom_response = jsonify(
            {"status": 401, "message": "No Token Provided"}), 401

    return custom_response


@OFFICE_BP_V2.route("", methods=["POST"])
def create_an_office():
    """ Create a political office """
    custom_response = None
    auth_header = request.headers.get('Authorization')
    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)
        admin_record = DatabaseManager().\
            fetch_a_record_by_id_from_a_table("users", "is_admin", True)

        if not isinstance(decoded_token, str):
            office_reg_data = request.get_json(force=True)
            sample_office = PoliticalOffices(office_reg_data)

            if DatabaseManager().is_admin(decoded_token) is False:
                custom_response = jsonify({
                    "status": 401,
                    "message": "Only Admin can create an office"}), 401

            elif len(office_reg_data) != 2:
                custom_response = jsonify(
                    sample_office.invalid_office_creation_data_fields_response
                ), 400

            elif sample_office.validate_office_reg_data() is None:
                custom_response = jsonify(sample_office.create_office()), 201

            else:
                custom_response = sample_office.validate_office_reg_data()

        else:
            custom_response = jsonify({'message': decoded_token}), 401

    else:
        custom_response = jsonify(
            {"status": 401, "message": "No Token Provided"}), 401

    return custom_response


@OFFICE_BP_V2.route("/<int:office_id>", methods=["GET"])
def office_fetch(office_id):
    """Fetch political office by ID """
    custom_response = None
    auth_header = request.headers.get('Authorization')
    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)

        if not isinstance(decoded_token, str):
            if office_id >= 1:
                if DatabaseManager().\
                    lookup_whether_entity_exists_in_a_table_by_attrib(
                        "offices", "office_id", office_id) is True:
                    raw_office = DatabaseManager().\
                        fetch_a_record_by_id_from_a_table(
                            "offices", "office_id", office_id
                    )
                    office = {}
                    office["Office ID"] = raw_office[0]["office_id"]
                    office["Office Name"] = raw_office[0]["name"]
                    office["Office Type"] = raw_office[0]["type"]
                    office["Registration Timestamp"] = \
                        raw_office[0]["registration_timestamp"]
                    custom_response = jsonify({
                        "status": 200, "Political Office": [office]
                    })
                else:
                    custom_response = jsonify(
                        ValidationHelper().id_out_of_range_response
                    ), 416
            else:
                custom_response = jsonify(
                    ValidationHelper().id_cannot_be_zero_response
                ), 400

        else:
            custom_response = jsonify({'message': decoded_token}), 401

    else:
        custom_response = jsonify(
            {"status": 401, "message": "No Token Provided"}), 401

    return custom_response
