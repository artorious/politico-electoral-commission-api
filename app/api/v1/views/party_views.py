#!/usr/bin/env python3
""" Political party views """
from flask import Blueprint, jsonify, request
from app.api.v1.models.party_models import PoliticalParties
from app.api.v1.validation_script import (
    more_data_fields_response, few_data_fields_response,
    empty_data_field_response, id_out_of_range_response,
    id_cannot_be_zero_response
)
PARTY_BP_V1 = Blueprint("v1_party", __name__, url_prefix="/api/v1")


@PARTY_BP_V1.route("/parties", methods=["GET"])
def fetch_all_parties():
    """ Fetch all political parties """
    return jsonify(PoliticalParties.get_all_parties())


@PARTY_BP_V1.route("/parties", methods=["POST"])
def create_a_party():
    """ Fetch all political parties """
    custom_response = None

    party_reg_data = request.get_json(force=True)
    sample_party = PoliticalParties(party_reg_data)

    if len(party_reg_data) > 4:
        custom_response = jsonify(more_data_fields_response), 400
    elif len(party_reg_data) < 4:
        custom_response = jsonify(few_data_fields_response), 400

    elif sample_party.party_reg_validation() is None:
        custom_response = jsonify(sample_party.create_party()), 201
    else:
        custom_response = sample_party.party_reg_validation()
    return custom_response


@PARTY_BP_V1.route("/parties/<int:pid>", methods=["GET"])
def fetch_a_party(pid):
    """(Fetch a political party  by ID """
    custom_response = None
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

    return custom_response


@PARTY_BP_V1.route("/parties/<int:pid>", methods=["DELETE"])
def delete_a_party(pid):
    """DELETE a political party  by ID """
    custom_response = None
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

    if len(party_updates) != 1:
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
