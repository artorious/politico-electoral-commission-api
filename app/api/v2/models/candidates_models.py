#!/usr/bin/env python3
""" Data representation - Routines for user to interact with the API. """
import time
import json
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

        custom_msg = "Nope"
        try:
            party_name = self.candidate_reg_data["party_name"].title()
            user_email = self.candidate_reg_data["user_email"]

            self.cursor.execute(
                f"select * from parties where name like '{party_name}'")
            party_details = self.cursor.fetchall()
            party_id = party_details[0]["party_id"]

            self.cursor.execute(
                f"select * from users where email like '{user_email}'")
            user_details = self.cursor.fetchall()
            user_id = user_details[0]["user_id"]

            if self.lookup_whether_entity_exists_in_a_table_by_attrib(
                    "candidates", "user_id", user_id) is True:
                custom_msg = jsonify({
                    "status": 409,
                    "Error": "Candidate already registered"})
            else:

                self.cursor.execute("""
                INSERT INTO candidates (\
                candidate_id, office_id, user_id, party_id,
                registration_timestamp)
                VALUES (DEFAULT, %s, %s, %s, %s) RETURNING candidate_id;""", (
                    self.office_id, user_id, party_id, time.asctime(time_obj)
                ))
                last_id = self.cursor.fetchall()

                custom_msg = jsonify({
                    "status": 201,
                    "candidate Registration": [{
                        "Candidate id": last_id[0]["candidate_id"],
                        "user": f" {user_email} registered as a candidate"}]})
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

        finally:
            return custom_msg

    def validate_candidate_reg_data(self):
        """ Validate Candidate Reg data """

        custom_response = None
        value_list = list(self.candidate_reg_data.values())

        if self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "offices", "office_id", self.office_id) is False:
            custom_response = jsonify(self.office_id_out_of_range_response), 404

        elif self.check_for_expected_keys_in_user_input(
                self.candidate_reg_data, ["user_email", "party_name"]
        ) is False:
            custom_response = jsonify(
                self.invalid_candidate_creation_data_fields_response), 400

        elif self.check_for_expected_value_types_in_user_input(
                self.candidate_reg_data) is False:
            custom_response = jsonify(self.unexpected_data_types_resp), 422

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "parties", "name",
                self.candidate_reg_data["party_name"]) is False:
            custom_response = jsonify(self.unknown_party_response), 422

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "users", "email", self.candidate_reg_data["user_email"]
        ) is False:
            custom_response = jsonify(self.unknown_user_response), 422

        return custom_response


def create_a_petition(self, office, cover_letter, evidence):
        """ Create/Register a petition """
        time_obj = time.localtime(time.time())
        try:
            self.cursor.execute("""
            INSERT INTO petitions (
            petition_id, office, cover_letter, evidence,
            registration_timestamp)
            VALUES (DEFAULT, %s, %s, %s, %s)
            RETURNING petition_id, office, cover_letter,
            evidence, registration_timestamp;""", (

                office, cover_letter,
                evidence, time.asctime(time_obj)
            ))
            new_petition = self.cursor.fetchall()
            custom_msg = new_petition

        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

        finally:
            return custom_msg
