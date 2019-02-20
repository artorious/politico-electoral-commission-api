#!/usr/bin/env python3
""" Routes Candidate Information """

from flask import Blueprint, jsonify, request
from app.api.v2.models.candidates_models import Candidates
from app.api.v2.models.votes_model import VoteHandler
from app.api.v2.models.database_models import DatabaseManager
from app.api.v2.models.validation_helper import ValidationHelper

BASE_BP_V2 = Blueprint("v2_base", __name__, url_prefix="/api/v2")


@BASE_BP_V2.route("/office/<int:oid>/register", methods=["POST"])
def create_candidate(oid):
    """ Create a candidate """
    custom_response = None
    auth_header = request.headers.get('Authorization')

    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)
        if not isinstance(decoded_token, str):
            if DatabaseManager().is_admin(decoded_token) is True:

                candidate_reg_data = request.get_json(force=True)
                sample_candidate = Candidates(oid, candidate_reg_data)

                if len(candidate_reg_data) > 2:
                    custom_response = jsonify(
                        sample_candidate.more_data_fields_response), 400

                elif len(candidate_reg_data) < 2:
                    custom_response = jsonify(
                        sample_candidate.few_data_fields_response), 400

                elif sample_candidate.validate_candidate_reg_data() is None:
                    custom_response = jsonify(
                        sample_candidate.create_a_candidate()), 201

                else:
                    custom_response = \
                        sample_candidate.validate_candidate_reg_data()
            else:
                custom_response = jsonify({
                    "user": decoded_token,
                    'message': "Restricted Access. Admin only"}), 401

        else:
            custom_response = jsonify({
                "user": decoded_token,
                'message': "Invalid Token"}), 401

    else:
        custom_response = jsonify(
            {"status": 401, "message": "No Token Provided"}), 401

    return custom_response


@BASE_BP_V2.route("/office/open", methods=["GET"])
def fetch_all_open_offices():
    """ Fetch all political offices (GET) """

    auth_header = request.headers.get('Authorization')
    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)

        if not isinstance(decoded_token, str):
            raw_candidates = \
                DatabaseManager().fetch_all_records_in_a_table("candidates")

            if raw_candidates == []:
                custom_response = jsonify({
                    "data": "The Candidate list is empty", "status": 200
                }), 200
            else:
                data = []
                for record in raw_candidates:
                    sample = {}
                    sample["Candidate ID"] = record["cid"]
                    sample["User ID"] = record["uid"]
                    sample["Office ID"] = record["oid"]
                    sample["Party ID"] = record["pid"]
                    sample["Registration Timestamp"] = \
                        record["registration_timestamp"]
                    data.append(sample)
                custom_response = jsonify({
                    "status": 200, "Registered Candidates": data
                }), 200
        else:
            custom_response = jsonify({'message': decoded_token}), 401

    else:
        custom_response = jsonify(
            {"status": 401, "message": "No Token Provided"}), 401

    return custom_response


@BASE_BP_V2.route("/votes/", methods=["POST"])
def vote_office():
    """ Vote for  a political office """
    custom_response = None
    auth_header = request.headers.get('Authorization')
    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)

        if not isinstance(decoded_token, str):
            raw_vote_data = request.get_json(force=True)
            sample_vote = VoteHandler(raw_vote_data)

            if len(raw_vote_data) > 4:
                custom_response = jsonify(
                    sample_vote.more_data_fields_response), 400
            elif len(raw_vote_data) < 4:
                custom_response = jsonify(
                    sample_vote.few_data_fields_response), 400
            elif sample_vote.validate_vote_data() is None:
                response = sample_vote.cast_a_vote()
                if "duplicate_error" in response:
                    custom_response = jsonify(response), 409
                else:

                    custom_response = jsonify(response), 201
            else:
                custom_response = sample_vote.validate_vote_data()

        else:
            custom_response = jsonify({'message': decoded_token}), 401

    else:
        custom_response = jsonify(
            {"status": 401, "message": "No Token Provided"}), 401

    return custom_response
