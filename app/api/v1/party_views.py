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
                "status": 400,
                "error": "Bad Query - More data fields than expected"
            }), 400
        elif len(party_reg_data) < 4:
            custom_response = jsonify({
                "status": 400,
                "error": "Bad Query - Fewer data fields than expected"
            }), 400
        elif sample_party.check_for_expected_value_types() is False:
            custom_response = jsonify({
                "status": 422,
                "error": "Unprocessable Entity - Invalid value in data field"
            }), 422
        elif sample_party.check_for_any_empty_fields() is False:
            custom_response = jsonify({
                "status": 422,
                "error": "Empty data field"
            }), 422
        elif sample_party.check_whether_party_exists(
                party_reg_data["name"]) is True:
            custom_response = jsonify({
                "status": 409,
                "error": "Conflict - Party already exists"
            }), 409
        else:
            custom_response = jsonify(sample_party.create_party()), 201

    elif request.method == "GET":
        custom_response = jsonify(PoliticalParties.get_all_parties())

    else:
        pass

    return custom_response


@BASE_BP_V1.route("/parties/<int:pid>", methods=["GET"])
def party(pid):
    """
    GET -> Fetch political party by ID
    """
    custom_response = None

    if request.method == "GET":

        if isinstance(pid, int) and pid >= 1:
            if PoliticalParties.check_id_exists(pid) is True:
                custom_response = jsonify({
                    "status": 200,
                    "data": PoliticalParties.fetch_a_party(pid)
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


@BASE_BP_V1.route("/parties/<int:pid>/name", methods=["PATCH"])
def party_manager(pid):
    """ Edit politcal party  name by ID"""
    # request user data
    # if "name" in user data
        # if len of user data is 1
            # if id is not 0
                # if id exists in list
                    # try editing the party with user data-> to model
                    #return csm msg
                # id does not exist
                    # cstm error msg
            # else if id is zero
                #cstm error msg
        # else if len of user data > 1
            # cstom message
    # else if "name" not in userdata
        # custom msg
    pass

# Response Spec:

# {
    # “status” : Integer() ,
    # “data” : [
         # {
              # “id” : Integer ,
              # “name” : String (new name)
           # }
    # ]
# }

# or

# {
    # “status” : integer ,
    # “error” : “String: relevant-error-message”
# }
