#!/usr/bin/env python3
""" Routes Candidate Information """
import time
import psycopg2
from flask import Blueprint, jsonify, request
from app.api.v2.models.candidates_models import Candidates
from app.api.v2.models.votes_model import VoteHandler
from app.api.v2.models.database_models import DatabaseManager
from app.api.v2.models.validation_helper import ValidationHelper

BASE_BP_V2 = Blueprint("v2_base", __name__, url_prefix="/api/v2")


@BASE_BP_V2.route("/office/<int:office_id>/register", methods=["POST"])
def create_candidate(office_id):
    """ Create a candidate """
    custom_response = None
    auth_header = request.headers.get('Authorization')

    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)
        if not isinstance(decoded_token, str):
            if DatabaseManager().is_admin(decoded_token) is True:

                candidate_reg_data = request.get_json(force=True)
                sample_candidate = Candidates(office_id, candidate_reg_data)

                if len(candidate_reg_data) != 2:
                    custom_response = jsonify(
                        sample_candidate.
                        invalid_candidate_creation_data_fields_response
                    ), 400

                elif sample_candidate.validate_candidate_reg_data() is None:
                    custom_response = sample_candidate.create_a_candidate()

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

                    user_details = DatabaseManager().\
                        fetch_a_record_by_id_from_a_table(
                            "users", "user_id", record["user_id"])
                    office_details = DatabaseManager().\
                        fetch_a_record_by_id_from_a_table(
                        "offices", "office_id", record["office_id"])
                    party_details = DatabaseManager().\
                        fetch_a_record_by_id_from_a_table(
                        "parties", "party_id", record["party_id"])

                    sample = {}
                    sample["Candidate ID"] = record["candidate_id"]
                    sample["User ID"] = record["user_id"]
                    sample["Candidate Names"] =\
                        f"{user_details[0][1]} {user_details[0][2]}"
                    sample["Office ID"] = record["office_id"]
                    sample["Office Name"] = office_details[0][1]
                    sample["Office Type"] = office_details[0][2]
                    sample["Party ID"] = record["party_id"]
                    sample["Party Name"] = party_details[0][1]
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
            sample_vote = VoteHandler(raw_vote_data, decoded_token)

            if len(raw_vote_data) != 3:
                custom_response = jsonify(
                    sample_vote.invalid_vote_fields_response), 400

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


@BASE_BP_V2.route("/office/<int:office_id>/result", methods=["GET"])
def vote_tally(office_id):
    """ Collate and fetch the result of specific office."""
    custom_response = None

    cur = DatabaseManager()
    cur.cursor.execute(f"select * from offices where office_id={office_id}")

    office_check = cur.cursor.fetchall()
    if office_check == []:
        custom_response = jsonify({
            "status": 404,
            "error": f"Office id {office_id} doesnt exist in our records"}), 404
    else:

        vote_info = cur.fetch_a_record_by_id_from_a_table(
            "votes", "office_id", office_id)

        cur.cursor.execute(
            f"SELECT COUNT(*) FROM votes where office_id={office_id};")
        results = cur.cursor.fetchall()

        if vote_info == []:
            custom_response = jsonify({
                "status": 200,
                office_check[0]["type"]: "No data available"}), 200
        else:
            data = []
            for i in vote_info:
                data.append({
                    "office": i[3], "candidate": i[2], "results": i[0]})
            custom_response = jsonify({
                "status": 200, office_check[0]["type"]: data}), 200

    return custom_response


@BASE_BP_V2.route("/petitions", methods=["POST"])
def make_petition():
    """ Petition to challenge an election """
    custom_response = None
    auth_header = request.headers.get('Authorization')

    if auth_header is not None:
        access_token = auth_header.split(" ")[1]
        decoded_token = ValidationHelper.decode_token(access_token)

        if not isinstance(decoded_token, str):
            if DatabaseManager().is_admin(decoded_token) is True:

                petition_data = request.get_json()
                if petition_data is None:
                    custom_response = jsonify(
                        'Unsupported Media-Type. Expected json'), 415
                else:
                    if len(petition_data) > 3:
                        custom_response = jsonify(
                            ValidationHelper.more_data_fields_response), 400

                    elif len(petition_data) < 3:
                        custom_response = jsonify(
                            ValidationHelper.few_data_fields_response), 400
                    else:
                        office = petition_data['office']
                        letter = petition_data["cover_letter"]
                        evidence = ['evidence']
                        cur = DatabaseManager()
                        time_obj = time.localtime(time.time())
                        cur.cursor.execute("""
                            INSERT INTO petitions (
                            petition_id, office, cover_letter, evidence,
                            registration_timestamp)
                            VALUES (DEFAULT, %s, %s, %s, %s)
                            RETURNING petition_id, office, cover_letter,
                            evidence, registration_timestamp;""", (
                                office, letter, evidence, time.asctime(time_obj)
                            ))

                        response = cur.cursor.fetchall()
                        petition = {}
                        petition["petition_id"] = response[0]["petition_id"]
                        petition["office"] = response[0]["office"]
                        petition["cover_letter"] = response[0]["cover_letter"]
                        petition["evidence"] = response[0]["evidence"]
                        petition["registration_timestamp"] = \
                            response[0]["registration_timestamp"]

                        custom_response = jsonify({
                            "status": 201, "petition": petition})

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
