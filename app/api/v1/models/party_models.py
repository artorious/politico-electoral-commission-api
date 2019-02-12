#!/usr/bin/env python3
""" Data representation - Routines for user to interact with the API. """

import time
from flask import jsonify
from app.api.v1.validation_script import (
    more_data_fields_response, few_data_fields_response,
    unprocessable_data_response, empty_data_field_response,
    entity_already_exists_response, id_out_of_range_response,
    id_cannot_be_zero_response, ValidationHelper
)


POLITICAL_PARTIES = []
PARTY_COUNT = 1


class PoliticalParties(ValidationHelper):
    """ Methods to model party information """
    def __init__(self, party_reg_data):
        self.party_reg_data = party_reg_data

    def create_party(self):
        """ Validate, append, return custom message """
        global POLITICAL_PARTIES, PARTY_COUNT
        time_stamp = time.localtime(time.time())
        self.party_reg_data["id"] = PARTY_COUNT
        PARTY_COUNT += 1
        self.party_reg_data["registered on"] = time.asctime(time_stamp)
        POLITICAL_PARTIES.append(self.party_reg_data)
        custom_msg = {
            "status": 201,
            "data": [{
                "id": self.party_reg_data["id"],
                "name": self.party_reg_data["name"]
                }]
            }
        return custom_msg

    def check_for_expected_keys(self, list_of_expected_keys):
        """ (dict, list) -> bool
            Checks for dict-key equality
        """
        return list(self.party_reg_data.keys()) == list_of_expected_keys

    def check_for_any_empty_fields(self):
        """ (dict) -> bool
            checks for empty strings
        """
        custom_msg = None
        if "" in self.party_reg_data.values():
            custom_msg = False
        elif (
                self.party_reg_data["name"].isspace() or
                self.party_reg_data["hqAddress"].isspace() or
                self.party_reg_data["logoUrl"].isspace() or
                self.party_reg_data["Party members"] < 1
        ):
            custom_msg = False
        else:
            custom_msg = True
        return custom_msg

    def check_for_expected_value_types(self):
        """ Check for expected value types"""
        custom_msg = None
        if (
                isinstance(self.party_reg_data["name"], str) and
                isinstance(self.party_reg_data["hqAddress"], str) and
                isinstance(self.party_reg_data["logoUrl"], str) and
                isinstance(self.party_reg_data["Party members"], int)
        ):
            custom_msg = True
        else:
            custom_msg = False
        return custom_msg


    def check_whether_party_exists(self, name):
        """ Handle double registartion """
        global POLITICAL_PARTIES
        return super().check_whether_entity_exists(name, POLITICAL_PARTIES)

    @staticmethod
    def get_all_parties():
        """ Fetch all parties """
        global POLITICAL_PARTIES
        custom_msg = None

        if POLITICAL_PARTIES == []:
            custom_msg = {
                "status": 200,
                "data": "The Party list is empty"
            }

        else:
            custom_msg = {
                "status": 200,
                "data": POLITICAL_PARTIES
            }
        return custom_msg

    @staticmethod
    def check_id_exists(pid):
        """ Check that provided id """
        global POLITICAL_PARTIES

        if pid in [party["id"] for party in POLITICAL_PARTIES]:
            return True
        else:
            return False

    @staticmethod
    def fetch_a_party(pid):
        """ Fetch a political party by ID"""
        global POLITICAL_PARTIES
        return [party for party in POLITICAL_PARTIES if party['id'] == pid]

    @staticmethod
    def check_for_valid_party_name(name):
        """ check name is not empty string, space & longer than 1 charaster"""
        if isinstance(name, str):
            return len(name.strip()) < 1
        else:
            return False

    @staticmethod
    def edit_party(user_data, pid):
        """ Edit apolitical party """
        global POLITICAL_PARTIES
        for party in POLITICAL_PARTIES:
            if party['id'] == pid:
                party['name'] = user_data["name"]

        return [{"id": pid, "name": user_data["name"]}]

    @staticmethod
    def delete_party(pid):
        """ Delete a political party by ID"""
        global POLITICAL_PARTIES
        POLITICAL_PARTIES = [party for party in POLITICAL_PARTIES if party['id'] != pid]
        return {
        "status": 200, "data": [
            {"message": f"Party No. {pid} deleted succesfully"}
            ]
        }

    def party_reg_validation(self):
        custom_response = None
        if self.check_for_expected_value_types() is False:
            custom_response = jsonify(unprocessable_data_response), 422
        elif self.check_for_any_empty_fields() is False:
            custom_response = jsonify(empty_data_field_response), 422
        elif self.check_whether_party_exists(
            self.party_reg_data["name"]) is True:
            custom_response = jsonify(entity_already_exists_response), 409
        return custom_response
