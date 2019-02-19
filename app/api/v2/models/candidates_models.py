#!/usr/bin/env python3
""" Data representation - Routines for user to interact with the API. """
import time
import psycopg2
from flask import jsonify
from app.api.v2.models.validation_helper import ValidationHelper


class Candidates(ValidationHelper):
    """ Candidate methods"""
    def __init__(self, office_id, candidate_reg_data):

        self.candidate_reg_data = candidate_reg_data
        self.office_id = office_id
        super().__init__()

    def create_a_candidate(self):
        """ Create/Register Candidate """
        time_obj = time.localtime(time.time())
        custom_msg = None
        try:
            self.cursor.execute("""
            INSERT INTO candidates (\
            cid, oid, uid, pid, registration_timestamp)
            VALUES (DEFAULT, %s, %s, %s, %s) RETURNING cid;""", (
                self.office_id,
                self.candidate_reg_data["user_id"],
                self.candidate_reg_data["party_id"],
                time.asctime(time_obj)
            ))
            last_id = self.cursor.fetchall()

            custom_msg = {"status": 201, "candidate": [{
                "id": last_id[0]["cid"],
                "user": self.candidate_reg_data["user_id"]
            }]}

        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

        finally:
            return custom_msg

    def validate_candidate_reg_data(self):
        """ Validate Candidate Reg data """

        custom_response = None
        value_list = list(self.candidate_reg_data.values())

        print(value_list)
        if self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "offices", "oid", self.office_id) is False:
            custom_response = jsonify(self.unprocessable_office_response), 422
        elif self.check_for_expected_keys_in_user_input(
                self.candidate_reg_data, ["office_id", "user_id", "party_id"]
        ) is False:
            custom_response = jsonify(self.unkown_fields_response), 400

        elif self.check_list_contains_only_integers(value_list) is False:
            custom_response = jsonify(
                self.unprocessable_data_type_response), 422

        elif self.check_list_contains_only_positive_integers(
                value_list) is False:
            custom_response = jsonify(self.id_cannot_be_zero_response), 400

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "parties", "pid", self.candidate_reg_data["party_id"]) is False:
            custom_response = jsonify(self.unprocessable_party_response), 422

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "users", "uid", self.candidate_reg_data["user_id"]
        ) is False:
            custom_response = jsonify(self.unprocessable_user_response), 422



        return custom_response
