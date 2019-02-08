#!/usr/bin/env python3
""" Routes Office Information """

from flask import Blueprint, jsonify, request
from app.api.v1.office_models import PoliticalOffices

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
            custom_response = jsonify({
                "status": 400,
                "error": "Bad Query - More data fields than expected"
            }), 400
        elif len(office_reg_data) < 2:
            custom_response = jsonify({
                "status": 400,
                "error": "Bad Query - Fewer data fields than expected"
            }), 400

        elif sample_office.check_for_expected_keys_present(
                ["name", "type"]) is False:
            custom_response = jsonify({
                "status": 422,
                "error": "Unprocessable Entity - Invalid value in data field"
            }), 422
        elif sample_office.check_for_expected_type_of_office(
                ["Federal", "Legislative", "State", "Local Government"]
                ) is False:
            custom_response = jsonify({
                "status": 422,
                "error": "Unprocessable Entity - Invalid value in data field"
            }), 422
        elif sample_office.check_any_for_empty_fields() is False:
            custom_response = jsonify({
                "status": 422,
                "error": "Unprocessable Entity - Invalid value in data field"
            }), 422
        elif sample_office.check_whether_office_exists(
                office_reg_data["name"]) is True:
            custom_response = jsonify({
                "status": 409,
                "error": "Conflict - Office already exists"
            }), 409
        else:
            custom_response = jsonify(sample_office.create_office()), 201
    else:
        custom_response = jsonify(PoliticalOffices.get_all_offices())

    return custom_response

@OFFICE_BP_V1.route("/offices/<int:pid>", methods=["GET"])
def office(pid):
    """Fetch political office by ID """
    custom_response = None

    if request.method == "GET":

        if isinstance(pid, int) and pid >= 1:
            if PoliticalOffices.check_id_exists(pid) is True:
                custom_response = jsonify({
                    "status": 200,
                    "data": PoliticalOffices.fetch_an_office(pid)
                }), 200
            else:
                custom_response = jsonify({
                    "status": 416,
                    "error": "ID out of range. Requested Range Not Satisfiable"
                }), 416
        elif pid < 1:
            custom_response = jsonify({
                "status": "Failed",
                "error": "ID cannot be zero or negative"
            }), 400
    else:
        pass

    return custom_response

