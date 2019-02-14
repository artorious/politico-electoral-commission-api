#!/usr/bin/env python3
""" Political party views """
from flask import Blueprint, jsonify, request
from app.api.v2.models.party_models import PoliticalParties
PARTY_BP_V2 = Blueprint("v2_party", __name__, url_prefix="/api/v2")

@PARTY_BP_V2.route("/parties", methods=["GET"])
def fetch_all_parties():
    """ Fetch all political parties """
    pass


@PARTY_BP_V2.route("/parties", methods=["POST"])
def create_a_party():
    """ Fetch all political parties """
    custom_response = None
    party_reg_data = request.get_json(force=True)
    sample_party = PoliticalParties(party_reg_data)

    if len(party_reg_data) > 3:
        custom_response = jsonify(sample_party.more_data_fields_response), 400
    elif len(party_reg_data) < 3:
        custom_response = jsonify(sample_party.few_data_fields_response), 400
    elif sample_party.validate_party_reg_data() is None:
        custom_response = jsonify(sample_party.create_party()), 201
    else:
        custom_response = sample_party.validate_party_reg_data()
    return custom_response

@PARTY_BP_V2.route("/parties/<int:pid>", methods=["GET"])
def fetch_a_party(pid):
    """(Fetch a political party  by ID """
    pass


@PARTY_BP_V2.route("/parties/<int:pid>", methods=["DELETE"])
def delete_a_party(pid):
    """DELETE a political party  by ID """
    pass


@PARTY_BP_V2.route("/parties/<int:pid>/name", methods=["PATCH"])
def party_manager(pid):
    """ Edit politcal party  name by ID"""
    pass