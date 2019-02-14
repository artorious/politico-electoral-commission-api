#!/usr/bin/env python3
""" Methods to validate data """
from app.api.v2.models.database_models import DatabaseManager

class ValidationHelper(DatabaseManager):
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
    id_out_of_range_response = {
        "status": 416, "error": "Entity not in server. ID out of range."
    }
    unprocessable_data_response = {
        "status": 422, "error": "Unprocessable Entity - Invalid value in data field"
    }
    empty_data_field_response = {
        "status": 422, "error": "Empty data field"
    }

    def check_for_expected_keys_in_user_input(self, raw_data, cartegory):
        if cartegory == "party registration":
            return list(raw_data.keys()) == self.expected_party_fields
        else:
            pass

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
        elif cartegory  == "party update":
            if raw_data["name"].strip() == "" or raw_data["name"].isspace():
                custom_msg = False
            else:
                custom_msg = True

        return custom_msg

    def check_for_expected_value_types_in_user_input(self, raw_data, cartegory):
        """ Check for expected value types"""
        custom_msg = None
        item_values = list(raw_data.values())
        if cartegory == "party registration":
            custom_msg = all(isinstance(item, str) for item in item_values)
        elif cartegory  == "party update":
            custom_msg = isinstance(raw_data["name"], str)
        return custom_msg

    def check_for_expected_no_of_fields(self, raw_data, cartegory):
        pass
