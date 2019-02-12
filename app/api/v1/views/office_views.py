#!/usr/bin/env python3
""" Routes Office Information """

from flask import Blueprint, jsonify, request
from app.api.v1.models.office_models import PoliticalOffices
from app.api.v1.validation_script import (
    more_data_fields_response, few_data_fields_response,
    id_out_of_range_response, id_cannot_be_zero_response
)

OFFICE_BP_V1 = Blueprint("v1_office", __name__, url_prefix="/api/v1")


@OFFICE_BP_V1.route("/offices", methods=["GET"])
def fetch_all_offices():
    """ Fetch all political offices (GET) """
    dummy_instance = PoliticalOffices()
    return jsonify(dummy_instance.get_all_offices())


@OFFICE_BP_V1.route("/offices", methods=["POST"])
def create_an_offices():
    """ Create a political office """
    custom_response = None
    office_reg_data = request.get_json(force=True)
    sample_office = PoliticalOffices(office_reg_data)
    if len(office_reg_data) > 2:
        custom_response = jsonify(more_data_fields_response), 400
    elif len(office_reg_data) < 2:
        custom_response = jsonify(few_data_fields_response), 400
    elif sample_office.office_reg_validation() is None:
        custom_response = jsonify(sample_office.create_office()), 201
    else:
        custom_response = sample_office.office_reg_validation()

    return custom_response


@OFFICE_BP_V1.route("/offices/<int:pid>", methods=["GET"])
def office(pid):
    """Fetch political office by ID """
    custom_response = None
    dummy_instance = PoliticalOffices()
    if pid >= 1:
        if dummy_instance.check_id_exists(pid) is True:
            custom_response = jsonify({
                "status": 200,
                "data": PoliticalOffices.fetch_an_office(pid)
            }), 200
        else:
            custom_response = jsonify(id_out_of_range_response), 416
    elif pid < 1:
        custom_response = jsonify(id_cannot_be_zero_response), 400

    return custom_response
