#!/usr/bin/env python3
""" Routes Office Information """

from flask import Blueprint, jsonify, request
from app.api.v1.models.office_models import PoliticalOffices
from app.api.v1.views.response_vars import (
    more_data_fields_response, few_data_fields_response,
    unprocessable_data_response, entity_already_exists_response,
    id_out_of_range_response, id_cannot_be_zero_response, expected_offices
)

OFFICE_BP_V1 = Blueprint("v1_office", __name__, url_prefix="/api/v1")


@OFFICE_BP_V1.route("/offices", methods=["POST", "GET"])
def offices():
    """ Create a political office(POST) and Fetch all political offices (GET)
    """
    custom_response = None
    if request.method == "POST":
        office_reg_data = request.get_json(force=True)
        sample_office = PoliticalOffices(office_reg_data)
        if len(office_reg_data) > 2:
            custom_response = jsonify(more_data_fields_response), 400
        elif len(office_reg_data) < 2:
            custom_response = jsonify(few_data_fields_response), 400
        elif sample_office.check_for_expected_keys_present(
                ["name", "type"]) is False:
            custom_response = jsonify(unprocessable_data_response), 422
        elif sample_office.check_for_expected_type_of_office(
                expected_offices
                ) is False:
            custom_response = jsonify(unprocessable_data_response), 422
        elif sample_office.check_any_for_empty_fields() is False:
            custom_response = jsonify(unprocessable_data_response), 422
        elif sample_office.check_whether_office_exists(
                office_reg_data["name"]) is True:
            custom_response = jsonify(entity_already_exists_response), 409
        else:
            custom_response = jsonify(sample_office.create_office()), 201
    else:
        custom_response = jsonify(PoliticalOffices.get_all_offices())

    return custom_response


@OFFICE_BP_V1.route("/offices/<int:pid>", methods=["GET"])
def office(pid):
    """Fetch political office by ID """
    custom_response = None
    if pid >= 1:
        if PoliticalOffices.check_id_exists(pid) is True:
            custom_response = jsonify({
                "status": 200,
                "data": PoliticalOffices.fetch_an_office(pid)
            }), 200
        else:
            custom_response = jsonify(id_out_of_range_response), 416
    elif pid < 1:
        custom_response = jsonify(id_cannot_be_zero_response), 400

    return custom_response
