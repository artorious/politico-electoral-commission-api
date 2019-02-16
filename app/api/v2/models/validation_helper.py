#!/usr/bin/env python3
""" Methods to validate data """
from app.api.v2.models.database_models import DatabaseManager


class ValidationHelper(DatabaseManager):
    """ Methods that Validate user input"""
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
    def __init__(self):
        super().__init__()

    def check_for_expected_keys_in_user_input(
        self, raw_data, expected_party_fields
    ):
        """ (dict, list) -> bool
            Check for expected dict keys in user_input.
            Return True/False
        """
        return list(raw_data.keys()) == expected_party_fields

    def check_for_empty_strings_in_user_input(self, raw_data):
        """ Truthy """
        items_list = list(raw_data.values())
        return any(item.strip() == "" for item in items_list)

    def check_for_expected_value_types_in_user_input(self, raw_data):
        """ (dict) -> bool
            Check for expected value types
            eturn True/False
        """
        values_list = list(raw_data.values())
        return all(isinstance(item, str) for item in values_list)
    # TODO
    def validate_email_syntax(self):
        pass

    def validate_password_syntax(self):
        pass
