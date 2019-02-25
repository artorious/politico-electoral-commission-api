#!/usr/bin/env python3
""" Political party views """
from flask import Blueprint, jsonify, request
from app.api.v2.models.party_models import PoliticalParties
from app.api.v2.models.database_models import DatabaseManager
from app.api.v2.models.validation_helper import ValidationHelper

PARTY_BP_V2 = Blueprint("v2_party", __name__, url_prefix="/api/v2/parties")


@PARTY_BP_V2.route("", methods=["GET"])
def fetch_all_parties():
    """ Fetch all political parties """
    custom_response = None
    auth_header = request.headers.get('Authorization')
    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)

        if not isinstance(decoded_token, str):
            raw_parties = DatabaseManager().\
                fetch_all_records_in_a_table("parties")

            if raw_parties == []:
                custom_response = jsonify({
                    "data": "The Party list is empty", "status": 200
                }), 200
            else:
                data = []
                for record in raw_parties:
                    sample = {}
                    sample["Party ID"] = record["party_id"]
                    sample["Party Name"] = record["name"]
                    sample["HQ Address"] = record["hq_address"]
                    sample["Logo URL"] = record["logo_url"]
                    sample["Registration Timestamp"] =\
                        record["registration_timestamp"]
                    data.append(sample)
                custom_response = jsonify({
                    "status": 200, "Political Parties": data
                }), 200

        else:
            custom_response = jsonify({'message': decoded_token}), 401

    else:
        custom_response = jsonify(
            {"status": 401, "message": "No Token Provided"}), 401

    return custom_response


@PARTY_BP_V2.route("", methods=["POST"])
def create_a_party():
    """ Create a  political party """
    custom_response = None
    auth_header = request.headers.get('Authorization')

    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)

        if not isinstance(decoded_token, str):
            party_reg_data = request.get_json(force=True)

            sample_party = PoliticalParties(party_reg_data, decoded_token)

            if len(party_reg_data) != 3:
                custom_response = jsonify(
                    sample_party.invalid_party_creation_data_fields_response
                ), 400

            elif sample_party.validate_party_reg_data() is None:
                custom_response = jsonify(sample_party.create_party()), 201

            else:
                custom_response = sample_party.validate_party_reg_data()

        else:
            custom_response = jsonify({'message': decoded_token}), 401

    else:
        custom_response = jsonify(
            {"status": 401, "message": "No Token Provided"}), 401

    return custom_response


@PARTY_BP_V2.route("/<int:party_id>", methods=["GET"])
def fetch_a_party(party_id):
    """(Fetch a political party  by ID """
    custom_response = None
    auth_header = request.headers.get('Authorization')

    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)

        if not isinstance(decoded_token, str):
            if party_id >= 1:
                if DatabaseManager().\
                    lookup_whether_entity_exists_in_a_table_by_attrib(
                        "parties", "party_id", party_id) is True:
                    raw_party = DatabaseManager().\
                        fetch_a_record_by_id_from_a_table(
                        "parties", "party_id", party_id)
                    party = {}
                    party["Party ID"] = raw_party[0]["party_id"]
                    party["Party Name"] = raw_party[0]["name"]
                    party["HQ Address"] = raw_party[0]["hq_address"]
                    party["Logo URL"] = raw_party[0]["logo_url"]
                    party["Registration Timestamp"] = \
                        raw_party[0]["registration_timestamp"]
                    custom_response = jsonify({
                        "status": 200, "Political Party": [party]})
                else:
                    custom_response = jsonify(
                        ValidationHelper().party_id_out_of_range_response), 404
            else:
                custom_response = jsonify(
                    ValidationHelper().id_cannot_be_zero_response), 400
        else:
            custom_response = jsonify({'message': decoded_token}), 401

    else:
        custom_response = jsonify(
            {"status": 401, "message": "No Token Found."}), 401

    return custom_response


@PARTY_BP_V2.route("/<int:party_id>", methods=["DELETE"])
def delete_a_party(party_id):
    """DELETE a political party  by ID """
    custom_response = None
    auth_header = request.headers.get('Authorization')

    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)

        if not isinstance(decoded_token, str):
            if party_id < 1:
                custom_response = jsonify(
                    ValidationHelper().id_cannot_be_zero_response), 400

            elif DatabaseManager().\
                lookup_whether_entity_exists_in_a_table_by_attrib(
                        "parties", "party_id", party_id) is True:
                    party_details = DatabaseManager().\
                        fetch_a_record_by_id_from_a_table(
                            "parties", "party_id", party_id)
                    if party_details[0][4] == decoded_token or \
                            DatabaseManager().is_admin(decoded_token):

                        custom_response = jsonify({
                            "status": 200,
                            "message": DatabaseManager().delete_a_table_record(
                                "parties", party_id)}), 200
                    else:
                        custom_response = jsonify({
                            "status": 401,
                            "message": "Only Admin and user who created \
                                the party can delete"}), 401
            else:
                custom_response = jsonify(
                    ValidationHelper().party_id_out_of_range_response), 404
        else:
            custom_response = jsonify({'message': decoded_token}), 401

    else:
        custom_response = jsonify(
            {"status": 401, "message": "No Token Provided"}), 401
    return custom_response


@PARTY_BP_V2.route("/<int:party_id>/name", methods=["PATCH"])
def edit_party_name(party_id):
    """ Edit politcal party  name by ID"""
    custom_response = None
    auth_header = request.headers.get('Authorization')
    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)

        if not isinstance(decoded_token, str):
            party_updates = request.get_json(force=True)

            if len(party_updates) != 1:
                custom_response = jsonify(
                    ValidationHelper.
                    invalid_party_name_edit_data_fields_response
                ), 400

            elif party_id < 1:
                custom_response = jsonify(
                    ValidationHelper.party_id_cannot_be_zero_response
                ), 400

            elif ValidationHelper().\
                check_for_expected_value_types_in_user_input(
                    party_updates) is False:
                custom_response = jsonify(
                    ValidationHelper.unexpected_data_types_resp), 422

            elif ValidationHelper().check_for_empty_strings_in_user_input(
                    party_updates) is True:
                custom_response = jsonify(
                    ValidationHelper.empty_data_field_response
                ), 422

            elif DatabaseManager().\
                lookup_whether_entity_exists_in_a_table_by_attrib(
                    "parties", "party_id", party_id) is False:
                custom_response = jsonify(
                    ValidationHelper.party_id_out_of_range_response
                ), 404

            else:
                party_details = DatabaseManager().\
                    fetch_a_record_by_id_from_a_table(
                        "parties", "party_id", party_id)
                old_party_name = party_details[0][1]

                if party_details[0][4] == decoded_token or \
                        DatabaseManager().is_admin(decoded_token):
                    custom_response = jsonify({
                        "status": 200,
                        f"Edit {old_party_name} party":
                            [DatabaseManager().edit_a_table_record(
                                "parties", party_id, party_updates)]
                        }), 200
                else:
                    custom_response = jsonify({
                        "status": 401,
                        "message": "Only Admin and user who created the \
                            party can edit"}), 401

        else:
            custom_response = jsonify({'message': decoded_token}), 401

    else:
        custom_response = jsonify(
            {"status": 401, "message": "No Token Provided"}), 401

    return custom_response
