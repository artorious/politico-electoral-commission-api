#!/usr/bin/env python3
""" Methods to validate data """
from app.api.v2.models.database_models import DatabaseManager


class ValidationHelper(DatabaseManager):
    """ Methods that Validate user input"""
    def __init__(self):
        super().__init__()
    """ Validation methods """
    expected_party_fields = ["name", "hq_address", "logo_url"]

    more_data_fields_response = {
        "status": 400, "error": "Bad Query - More data fields than expected"
    }
    few_data_fields_response = {
        "status": 400, "error": "Bad Query - Fewer data fields than expected"
    }
    id_cannot_be_zero_response = {
        "status": 400, "error": "ID cannot be zero or negative"
    }
    entity_already_exists_response = {
        "status": 409, "error": "Conflict - Entity already exists"
    }
    party_already_exists_response = {
        "status": 409, "error": "Conflict - Party already exists"
    }
    logo_already_exists_response = {
        "status": 409, "error": "Conflict - Logo already in use"
    }
    hq_already_exists_response = {
        "status": 409, "error": "Conflict - Address already in use"
    }
    id_out_of_range_response = {
        "status": 404, "error": "Entity not in server. ID out of range."
    }
    unprocessable_data_response = {
        "status": 422,
        "error": "Unprocessable Entity - Invalid value in data field"
    }
    empty_data_field_response = {
        "status": 422, "error": "Empty data field"
    }

    def check_for_expected_keys_in_user_input(
        self, raw_data, expected_party_fields
    ):
        """ (dict, list) -> bool
            Check for expected dict keys in user_input.
            Return True/False
        """
        return list(raw_data.keys()) == expected_party_fields

    def check_for_empty_strings_in_user_input(self, raw_data, cartegory):
        """ Truthy """
        custom_msg = None
        if cartegory == "party registration":
            if "" in raw_data.values():
                custom_msg = False

            elif (
                raw_data["name"].isspace() or
                raw_data["hq_address"].isspace() or
                raw_data["logo_url"].isspace()
            ):
                custom_msg = False
            else:
                custom_msg = True
        elif cartegory == "party update":
            if raw_data["name"].strip() == "" or raw_data["name"].isspace():
                custom_msg = False
            else:
                custom_msg = True
        elif cartegory == "office registration":
            if "" in raw_data.values():
                custom_msg = False
            elif (
                raw_data["name"].isspace() or
                raw_data["type"].isspace()
            ):
                custom_msg = False
            else:
                custom_msg = True

        return custom_msg

    def check_for_expected_value_types_in_user_input(self, raw_data):
        """ (dict) -> bool
            Check for expected value types
            eturn True/False
        """
        values_list = list(raw_data.values())
        return all(isinstance(item, str) for item in values_list)

    def check_for_expected_no_of_fields(self, raw_data, cartegory):
        pass
