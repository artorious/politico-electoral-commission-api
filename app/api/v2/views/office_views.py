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
    raw_offices = DatabaseManager().fetch_all_records_in_a_table("offices")
    
    if raw_offices == []:
        custom_response = jsonify({"data": "The Office list is empty", "status": 200}), 200
    else:
        data = []
        for record in raw_offices:
            sample = {}
            sample["Office ID"] = record["oid"]
            sample["Office Name"] = record["name"]
            sample["Office Type"] = record["type"]
            sample["Registration Timestamp"] = record["registration_timestamp"]
            data.append(sample)
        custom_response = jsonify({"status": 200, "Political Offices": data}), 200
    return custom_response


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
    custom_response = None
    if oid >= 1:
        if DatabaseManager().lookup_whether_entity_exists_in_a_table_by_attrib("offices", "oid", oid) is True:
            raw_office = DatabaseManager().fetch_a_record_by_id_from_a_table("offices", "oid", oid)
            office = {}
            office["Office ID"] = raw_office[0]["oid"]
            office["Office Name"] = raw_office[0]["name"]
            office["Office Type"] = raw_office[0]["type"]
            office["Registration Timestamp"] = raw_office[0]["registration_timestamp"]
            custom_response = jsonify({"status": 200, "Political Office": [office]})
        else:
            custom_response = jsonify(ValidationHelper().id_out_of_range_response), 416
    else:
        custom_response = jsonify(ValidationHelper().id_cannot_be_zero_response), 400

    return custom_response
