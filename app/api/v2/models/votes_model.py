#!/usr/bin/env python3
""" Data representation - Routines for user to interact with the API. """
import time
import psycopg2
from flask import jsonify
from app.api.v2.models.validation_helper import ValidationHelper
from app.api.v2.models.database_models import DatabaseManager


class VoteHandler(ValidationHelper):
    """ vote methods"""
    def __init__(self, vote_reg_data, voter_id):

        self.vote_reg_data = vote_reg_data
        self.voter_id = voter_id
        super().__init__()

    def cast_a_vote(self):
        """ Cast a Vote for a Candidate """
        time_obj = time.localtime(time.time())

        custom_msg = "Nope"
        try:
            office_name = self.vote_reg_data["office_name"]
            party_name = self.vote_reg_data["party_name"]
            candidate = self.vote_reg_data["candidate_id"]

            cur = DatabaseManager()
            cur.cursor.execute(
                f"select * from offices where name like '{office_name}'")
            office_details = cur.cursor.fetchone()

            cur.cursor.execute(
                f"select * from parties where name like '{party_name}'")
            party_details = cur.cursor.fetchone()

            cur.cursor.execute(
                f"select * from users where user_id={self.voter_id}")
            voter_details = cur.cursor.fetchone()

            cur.cursor.execute(
                f"select * from candidates where candidate_id={candidate}")
            candidate_details = cur.cursor.fetchone()

            cur.cursor.execute(
                f"select user_id, office_id from votes where " +
                f"user_id={self.voter_id} and office_id={office_details[0]}")
            vote_check = cur.cursor.fetchall()
            if vote_check == []:

                self.cursor.execute("""
                INSERT INTO votes (\
                vote_id, candidate_id, user_id, office_id, party_id,
                registration_timestamp)
                VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING vote_id;""", (
                    self.vote_reg_data["candidate_id"],
                    self.voter_id,
                    office_details[0],
                    party_details[0],
                    time.asctime(time_obj)
                ))
                last_id = self.cursor.fetchall()

                custom_msg = {"status": 201, "Cast Vote": [{
                    "Vote id": last_id[0]["vote_id"],
                    "Candidate ID": candidate_details[0],
                    "Office": office_details[1],
                    "Voter": f"{voter_details[1]} {voter_details[2]}"
                }]}
            else:
                custom_msg = {
                    "status": 409,
                    "Vote duplication error":
                    "Voter has already voted for this office"}

        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

        finally:
            return custom_msg

    def validate_vote_data(self):
        """ Validate Candidate Reg data """

        custom_response = None

        value_list = list(self.vote_reg_data .values())

        if self.check_for_expected_keys_in_user_input(
                self.vote_reg_data,
                ["office_name", "candidate_id", "party_name"]
        ) is False:
            custom_response = jsonify(self.invalid_vote_fields_response), 400

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "candidates", "candidate_id",
                self.vote_reg_data["candidate_id"]) is False:
            custom_response = jsonify(self.invalid_cadidate_id_resp), 422

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "parties", "name", self.vote_reg_data["party_name"]) is False:
            custom_response = jsonify(self.invalid_party_name_resp), 422

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "offices", "name", self.vote_reg_data["office_name"]
        ) is False:
            custom_response = jsonify(self.invalid_office_name_resp), 422

        return custom_response
