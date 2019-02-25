#!/usr/bin/env python3
""" Data representation - Routines for user to interact with the API. """
import time
import psycopg2
from flask import jsonify
from app.api.v2.models.validation_helper import ValidationHelper


class PoliticalParties(ValidationHelper):
    """ Parties methods"""
    def __init__(self, party_reg_data, user_id):
        self.party_reg_data = party_reg_data
        self.creators_user_id = user_id
        super().__init__()

    def create_party(self):
        """ Create Political party """
        time_obj = time.localtime(time.time())
        custom_msg = None
        try:
            self.cursor.execute("""
            INSERT INTO parties (\
            party_id, name, hq_address, logo_url,
            registered_by, registration_timestamp)
            VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING party_id;""", (
                self.party_reg_data["name"].title(),
                self.party_reg_data["hq_address"].title(),
                self.party_reg_data["logo_url"],
                self.creators_user_id,
                time.asctime(time_obj)
            ))
            last_id = self.cursor.fetchall()

            custom_msg = {"status": 201, "party": [{
                "id": last_id[0]["party_id"],
                "name": self.party_reg_data["name"]
            }]}

        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

        finally:
            return custom_msg

    def validate_party_reg_data(self):
        """ Validate Party Registartion Data"""
        custom_response = None
        if self.check_for_expected_keys_in_user_input(
                self.party_reg_data, ["name", "hq_address", "logo_url"]
        ) is False:
            custom_response = jsonify(
                self.unknown_party_creation_data_field_response), 422

        elif self.check_for_expected_value_types_in_user_input(
                self.party_reg_data) is False:
            custom_response = jsonify(self.unexpected_data_types_resp), 422

        elif self.check_for_empty_strings_in_user_input(
                self.party_reg_data) is True:
            custom_response = jsonify(self.empty_data_field_response), 422

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "parties", "name", self.party_reg_data["name"]) is True:
            custom_response = jsonify(
                self.party_name_already_exists_response), 409

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "parties", "hq_address", self.party_reg_data["hq_address"]
        ) is True:
            custom_response = jsonify(
                self.party_hq_already_exists_response), 409

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "parties", "logo_url", self.party_reg_data["logo_url"]) is True:
            custom_response = jsonify(
                self.party_logo_already_exists_response), 409

        return custom_response
