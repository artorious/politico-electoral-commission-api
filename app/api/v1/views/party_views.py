#!/usr/bin/env python3
""" Political party views """
from flask import Blueprint, jsonify, request
from app.api.v1.models.party_models import PoliticalParties
from app.api.v1.views.response_vars import (
    more_data_fields_response, few_data_fields_response,
    unprocessable_data_response, empty_data_field_response,
    entity_already_exists_response, id_out_of_range_response,
    id_cannot_be_zero_response
)
PARTY_BP_V1 = Blueprint("v1_party", __name__, url_prefix="/api/v1")




@PARTY_BP_V1.route("/parties", methods=["POST", "GET"])
def parties():
    """
        Create a political party - POST
        Fetch all political parties - GET
    """
    custom_response = None
    if request.method == "GET":
        custom_response = jsonify(PoliticalParties.get_all_parties())
    else:
        party_reg_data = request.get_json(force=True)
        sample_party = PoliticalParties(party_reg_data)
        if len(party_reg_data) > 4:
            custom_response = jsonify(more_data_fields_response), 400
        elif len(party_reg_data) < 4:
            custom_response = jsonify(few_data_fields_response), 400
        elif sample_party.check_for_expected_value_types() is False:
            custom_response = jsonify(unprocessable_data_response), 422
        elif sample_party.check_for_any_empty_fields() is False:
            custom_response = jsonify(empty_data_field_response), 422
        elif sample_party.check_whether_party_exists(
                party_reg_data["name"]) is True:
            custom_response = jsonify(entity_already_exists_response), 409
        else:
            custom_response = jsonify(sample_party.create_party()), 201

    return custom_response


@PARTY_BP_V1.route("/parties/<int:pid>", methods=["GET", "DELETE"])
def party(pid):
    """(GET)Fetch and (DELETE) purge a political party  by ID """
    custom_response = None

    if request.method == "GET":

        if pid >= 1:
            if PoliticalParties.check_id_exists(pid) is True:
                custom_response = jsonify({
                    "status": 200,
                    "data": PoliticalParties.fetch_a_party(pid)
                }), 200
            else:
                custom_response = jsonify(id_out_of_range_response), 416
        else:
            custom_response = jsonify(id_cannot_be_zero_response), 400
    else:
        if pid >= 1:
            if PoliticalParties.check_id_exists(pid) is True:
                custom_response = jsonify({
                    "status": 200,
                    "data": PoliticalParties.delete_party(pid)
                }), 200
            else:
                custom_response = jsonify(id_out_of_range_response), 416
        else:
            custom_response = jsonify(id_cannot_be_zero_response), 400

    return custom_response


@PARTY_BP_V1.route("/parties/<int:pid>/name", methods=["PATCH"])
def party_manager(pid):
    """ Edit politcal party  name by ID"""
    custom_response = None
    party_updates = request.get_json(force=True)

    if "name" not in party_updates or len(party_updates) != 1:
        custom_response = jsonify(more_data_fields_response), 400
    elif pid < 1:
        custom_response = jsonify(id_cannot_be_zero_response), 400
    elif PoliticalParties.check_id_exists(pid) is False:
        custom_response = jsonify(id_out_of_range_response), 416
    elif PoliticalParties.check_for_valid_party_name(party_updates["name"]):
        custom_response = jsonify(empty_data_field_response), 422

    else:
        custom_response = jsonify({
            "status": 200,
            "data": PoliticalParties.edit_party(party_updates, pid)
            }), 200

    return custom_response
