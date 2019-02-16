#!/usr/bin/env python3
""" Data representation - Routines for user to interact with the API. """
import time
import psycopg2
from flask import jsonify
from app.api.v2.models.validation_helper import ValidationHelper


class PoliticalOffices(ValidationHelper):
    """ Office methods"""
    def __init__(self, office_reg_data):
        self.office_reg_data = office_reg_data
        super().__init__()

    def create_office(self):
        """ Create/Register Office """
        time_obj = time.localtime(time.time())
        custom_msg = None
        try:
            self.cursor.execute("""
            INSERT INTO offices (oid, name, type, registration_timestamp)
            VALUES (DEFAULT, %s, %s, %s) RETURNING oid;""", (
                self.office_reg_data["name"],
                self.office_reg_data["type"],
                time.asctime(time_obj)
            ))
            last_id = self.cursor.fetchall()

            custom_msg = {"status": 201, "office": [{
                "id": last_id[0]["oid"],
                "name": self.office_reg_data["name"],
                "type": self.office_reg_data["type"]
            }]}

        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

        finally:
            return custom_msg

    def validate_office_reg_data(self):
        """ Validate Office Reg data """
        custom_response = None
        cartegory = "office registration"
        if self.check_for_expected_keys_in_user_input(
                self.office_reg_data, ["name", "type"]
        ) is False:
            custom_response = jsonify(self.unprocessable_data_response), 422
        elif self.check_for_expected_value_types_in_user_input(
                self.office_reg_data) is False:
            custom_response = jsonify(self.unprocessable_data_response), 422
        elif self.check_for_empty_strings_in_user_input(
                self.office_reg_data, "office registration"
        ) is False:
            custom_response = jsonify(self.empty_data_field_response), 422
        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "offices", "name", self.office_reg_data["name"]
        ) is True:
            custom_response = jsonify(self.entity_already_exists_response), 409
        elif self.office_reg_data["type"] not in [
                "Federal", "Legislative", "State", "Local Government"
        ]:
            custom_response = jsonify(self.unprocessable_data_response), 422
        return custom_response
