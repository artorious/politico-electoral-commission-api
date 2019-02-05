#!/usr/bin/env python3
""" Political party views """

from flask import Blueprint, jsonify, request
from app.api.v1.party_models import PoliticalParties

BASE_BP_V1 = Blueprint("v1_base", __name__, url_prefix="/api/v1")


@BASE_BP_V1.route("/parties", methods=["POST", "GET"])
def parties():
    """
        Create a political party - POST
    """
    custom_response = None
    if request.method == "POST":
        party_reg_data = request.get_json(force=True)
        sample_party = PoliticalParties(party_reg_data)
        if len(party_reg_data) > 4:
            custom_response = jsonify({
                "status": "Bad Query",
                "error": "More data fields than expected"
            }), 400
        elif len(party_reg_data) < 4:
            custom_response = jsonify({
                "status": "Bad Query",
                "error": "Fewer data fields than expected"
            }), 400
        elif sample_party.check_for_expected_value_types() is False:
            custom_response = jsonify({
                "status": "Unprocessable Entity",
                "error": "Invalid value in data field"
            }), 422
        elif sample_party.check_for_any_empty_fields() is False:
            custom_response = jsonify({
                "status": "Unprocessable Entity",
                "error": "Empty data field"
            }), 422
        else:
            custom_response = jsonify(sample_party.create_party()), 201

    elif request.method == "GET":
        custom_response = jsonify(PoliticalParties.get_all_parties())

    else:
        pass

    return custom_response




@BASE_BP_V1.route("/parties/<int:id>", methods=["GET"])
def party(id):
    """
    GET -> Fetch political party by ID
    """
    custom_response = None
    if request.method == "GET":
        # TODO:
        # Check if interger and not empty : 400 ????
            # {
                # "status": "integer",
                # "error": "String: relevant-error-message"
            # }
        # Check if float: 400
            # {
                # "status": "integer",
                # "error": "String: relevant-error-message"
            # }
        # check if its less than 1 : 400
            # {
                # "status": "integer",
                # "error": "String: relevant-error-message"
            # }
        # call model with id

        pass
    else:
        pass


    return custom_response



