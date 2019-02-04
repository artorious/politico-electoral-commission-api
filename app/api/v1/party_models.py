#!/usr/bin/env python3
""" Data representation - Routines for user to interact with the API. """

import time

POLITICAL_PARTIES = []
PARTY_COUNT = 1


class PoliticalParties:
    """ Methods to model party information """
    def __init__(self, party_reg_data):
        self.party_reg_data = party_reg_data

    def create_party(self):
        """ Validate, append, return custom message """
        global POLITICAL_PARTIES, PARTY_COUNT
        custom_msg = None
        party_already_present = False
        for each_party in POLITICAL_PARTIES:
            if each_party["name"] == self.party_reg_data["name"]:
                party_already_present = True
        if party_already_present:
            custom_msg = {
                "status": "Failed",
                "error": "Party already exists"
            }
        else:
            time_stamp = time.localtime(time.time())
            self.party_reg_data["id"] = PARTY_COUNT
            PARTY_COUNT += 1
            self.party_reg_data["registered on"] = time.asctime(time_stamp)
            POLITICAL_PARTIES.append(self.party_reg_data)
            custom_msg = {
                "Status": "Success",
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

    def get_all_parties(self):
        """ Fetch all parties """

        pass
