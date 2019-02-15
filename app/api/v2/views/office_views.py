#!/usr/bin/env python3
""" Routes Office Information """

from flask import Blueprint, jsonify, request
from app.api.v2.models.office_models import PoliticalOffices
from app.api.v2.models.database_models import DatabaseManager
from app.api.v2.models.validation_helper import ValidationHelper

OFFICE_BP_V2 = Blueprint("v2_office", __name__, url_prefix="/api/v2")


@OFFICE_BP_V2.route("/offices", methods=["GET"])
def fetch_all_offices():
    """ Fetch all political offices (GET) """
    pass


@OFFICE_BP_V2.route("/offices", methods=["POST"])
def create_an_office():
    """ Create a political office """
    custom_response = None
    office_reg_data = request.get_json(force=True)
    sample_party = PoliticalOffices(office_reg_data)

    if len(office_reg_data) > 2:
        custom_response = jsonify(sample_party.more_data_fields_response), 400
    elif len(office_reg_data) < 2:
        custom_response = jsonify(sample_party.few_data_fields_response), 400
    elif sample_party.validate_office_reg_data() is None:
        custom_response = jsonify(sample_party.create_office()), 201
    else:
        custom_response = sample_party.validate_office_reg_data()
    return custom_response

@OFFICE_BP_V2.route("/offices/<int:oid>", methods=["GET"])
def office(oid):
    """Fetch political office by ID """
    pass
