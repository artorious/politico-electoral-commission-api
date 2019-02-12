#!/usr/bin/env python3
""" Models Office Information """
import time
from flask import jsonify
from app.api.v1.validation_script import (
    more_data_fields_response, few_data_fields_response,
    unprocessable_data_response, empty_data_field_response,
    entity_already_exists_response, id_out_of_range_response,
    id_cannot_be_zero_response, ValidationHelper
)

POLITICAL_OFFICES = []
OFFICE_COUNT = 1


class PoliticalOffices(ValidationHelper):
    """ Methods to handle office related data"""
    def __init__(self, office_reg_data=None):
        self.office_reg_data = office_reg_data

    def create_office(self):
        """ Creates a political office"""
        global POLITICAL_OFFICES, OFFICE_COUNT
        time_stamp = time.localtime(time.time())
        self.office_reg_data["id"] = OFFICE_COUNT
        OFFICE_COUNT += 1
        self.office_reg_data["Posted on"] = time.asctime(time_stamp)
        POLITICAL_OFFICES.append(self.office_reg_data)
        custom_msg = {
            "status": 201,
            "data": [{
                "id": self.office_reg_data["id"],
                "name": self.office_reg_data["name"],
                "type": self.office_reg_data["type"],
                }]
            }
        return custom_msg

    def check_for_expected_keys_present(self, list_of_expected_keys):
        """ Checks for the expected keys in user input"""
        return list(self.office_reg_data.keys()) == list_of_expected_keys

    def check_for_expected_type_of_office(self, list_of_expected_types):
        """ Checks for the expected values in the type key in user input"""
        return self.office_reg_data["type"] in list_of_expected_types

    def check_any_for_empty_fields(self):
        """ Returns True only if the expected values in office registration
            details are not empty strings, else False
        """
        custom_msg = None
        if "" in self.office_reg_data.values():
            custom_msg = False
        elif (
                self.office_reg_data["name"].isspace() or
                self.office_reg_data["type"].isspace()
        ):
            custom_msg = False
        else:
            custom_msg = True
        return custom_msg

    def check_for_only_expected_value_types(self):
        """ Returns True only if the expected value types in office registration
            details, else False
        """
        custom_msg = None
        if (
                isinstance(self.office_reg_data["name"], str) and
                isinstance(self.office_reg_data["type"], str)
        ):
            custom_msg = True
        else:
            custom_msg = False
        return custom_msg

    def check_whether_office_exists(self, name):
        """ Returns True if the office exists, else False"""
        global POLITICAL_OFFICES
        return super().check_whether_entity_exists(name, POLITICAL_OFFICES)

    def get_all_offices(self):
        """ Fetch all parties """
        global POLITICAL_OFFICES
        return super().fetch_all_entities(POLITICAL_OFFICES)

    @staticmethod
    def check_id_exists(pid):
        """ Check that provided id """
        global POLITICAL_OFFICES

        if pid in [office["id"] for office in POLITICAL_OFFICES]:
            return True
        else:
            return False

    @staticmethod
    def fetch_an_office(pid):
        """ Fetch a political office by ID"""
        global POLITICAL_OFFICES
        return [office for office in POLITICAL_OFFICES if office['id'] == pid]

    def office_reg_validation(self):
        custom_response = None
        if self.check_for_only_expected_value_types() is False:
            custom_response = jsonify(unprocessable_data_response), 422
        elif self.check_any_for_empty_fields() is False:
            custom_response = jsonify(empty_data_field_response), 422
        elif self.check_whether_office_exists(
            self.office_reg_data["name"]) is True:
            custom_response = jsonify(entity_already_exists_response), 409
        return custom_response


