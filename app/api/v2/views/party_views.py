#!/usr/bin/env python3
""" Political party views """
from flask import Blueprint, jsonify, request
from app.api.v2.models.party_models import PoliticalParties
from app.api.v2.models.database_models import DatabaseManager
from app.api.v2.models.validation_helper import ValidationHelper

PARTY_BP_V2 = Blueprint("v2_party", __name__, url_prefix="/api/v2")


@PARTY_BP_V2.route("/parties", methods=["GET"])
def fetch_all_parties():
    """ Fetch all political parties """
    raw_parties = DatabaseManager().fetch_all_records_in_a_table("parties")

    if raw_parties == []:
        custom_response = jsonify({
            "data": "The Party list is empty", "status": 200
        }), 200
    else:
        data = []
        for record in raw_parties:
            sample = {}
            sample["Party ID"] = record["pid"]
            sample["Party Name"] = record["name"]
            sample["HQ Address"] = record["hq_address"]
            sample["Logo URL"] = record["logo_url"]
            sample["Registration Timestamp"] = record["registration_timestamp"]
            data.append(sample)
        custom_response = jsonify({
            "status": 200, "Political Parties": data
        }), 200
    return custom_response


@PARTY_BP_V2.route("/parties", methods=["POST"])
def create_a_party():
    """ Fetch all political parties """
    custom_response = jsonify(None)
    party_reg_data = request.get_json(force=True)
    sample_party = PoliticalParties(party_reg_data)


    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]
    print("#########->",access_token)

    if access_token:
        uid = ValidationHelper.decode_token(access_token)
        if not isinstance(user_id, str):
            if len(party_reg_data) > 3:
                custom_response = jsonify(sample_party.more_data_fields_response), 400
            elif len(party_reg_data) < 3:
                custom_response = jsonify(sample_party.few_data_fields_response), 400

            elif sample_party.validate_party_reg_data() is None:
                custom_response = jsonify(sample_party.create_party()), 201
            else:
                custom_response = sample_party.validate_party_reg_data()
            return custom_response
    else:
        message = uid
        response = {'message': message}
        custom_response = jsonify(response), 401

    return custom_response


@PARTY_BP_V2.route("/parties/<int:pid>", methods=["GET"])
def fetch_a_party(pid):
    """(Fetch a political party  by ID """
    custom_response = None
    if pid >= 1:
        if DatabaseManager().lookup_whether_entity_exists_in_a_table_by_attrib(
                "parties", "pid", pid) is True:
            raw_party = DatabaseManager().fetch_a_record_by_id_from_a_table(
                "parties", "pid", pid)
            party = {}
            party["Party ID"] = raw_party[0]["pid"]
            party["Party Name"] = raw_party[0]["name"]
            party["HQ Address"] = raw_party[0]["hq_address"]
            party["Logo URL"] = raw_party[0]["logo_url"]
            party["Registration Timestamp"] = \
                raw_party[0]["registration_timestamp"]
            custom_response = jsonify({
                "status": 200, "Political Party": [party]})
        else:
            custom_response = jsonify(
                ValidationHelper().id_out_of_range_response), 404
    else:
        custom_response = jsonify(
            ValidationHelper().id_cannot_be_zero_response), 400

    return custom_response


@PARTY_BP_V2.route("/parties/<int:pid>", methods=["DELETE"])
def delete_a_party(pid):
    """DELETE a political party  by ID """
    custom_response = None
    if pid >= 1:
        if DatabaseManager().lookup_whether_entity_exists_in_a_table_by_attrib(
                "parties", "pid", pid) is True:
            custom_response = jsonify({
                "status": 200,
                "message": DatabaseManager().delete_a_table_record(
                    "parties", pid)
            }), 200
        else:
            custom_response = jsonify(
                ValidationHelper().id_out_of_range_response), 404
    else:
        custom_response = jsonify(
            ValidationHelper().id_cannot_be_zero_response), 400

    return custom_response


@PARTY_BP_V2.route("/parties/<int:pid>/name", methods=["PATCH"])
def edit_party_name(pid):
    """ Edit politcal party  name by ID"""
    custom_response = None
    party_updates = request.get_json(force=True)

    if len(party_updates) != 1:
        custom_response = jsonify(
            ValidationHelper.more_data_fields_response
        ), 400
    elif pid < 1:
        custom_response = jsonify(
            ValidationHelper.id_cannot_be_zero_response
        ), 400
    elif ValidationHelper().check_for_expected_value_types_in_user_input(
            party_updates) is False:
        custom_response = jsonify(
            ValidationHelper.unprocessable_data_response), 422
    elif ValidationHelper().check_for_empty_strings_in_user_input(
            party_updates) is True:
        custom_response = jsonify(
            ValidationHelper.empty_data_field_response
        ), 422
    elif DatabaseManager().lookup_whether_entity_exists_in_a_table_by_attrib(
            "parties", "pid", pid) is False:
        custom_response = jsonify(
            ValidationHelper.id_out_of_range_response
        ), 404
    else:
        custom_response = jsonify({
            "status": 200,
            "data": [DatabaseManager().edit_a_table_record(
                "parties", pid, party_updates)]
            }), 200
    return custom_response
