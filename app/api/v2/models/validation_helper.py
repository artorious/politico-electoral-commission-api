#!/usr/bin/env python3
""" Holds Methods to Validate App data """
import re
import jwt
from flask import current_app
from app.api.v2.models.database_models import DatabaseManager


class ValidationHelper(DatabaseManager):
    """ Methods that Validate user input"""

    invalid_signup_data_fields_response = {
        "status": 400,
        "error": "Invalid user input data (Signup data fields). Expected fields for 'first_name', 'last_name', 'other_name', 'email', 'telephone', 'passport_url', 'password' and 'confirm_password'. Please try again."
    }

    invalid_party_creation_data_fields_response = {
        "status": 400, "error": "Invalid user input data (Party creation data fields). Expected fields for 'name', 'hq_address' and 'logo_url'. Please try again."
    }

    invalid_candidate_creation_data_fields_response = {
        "status": 400, "error": "Invalid user input data (Candidate creation data fields). Expected fields for 'user_email', and 'party_name'. Please try again."
    }

    invalid_party_name_edit_data_fields_response = {
        "status": 400, "error": "Invalid user input data (Party name edit field). Expected field for 'name' only. Please try again."
    }

    invalid_office_creation_data_fields_response = {
        "status": 400, "error": "Invalid user input data (Office creation data fields). Expected fields for 'name' and 'type'. Please try again."
    }

    invalid_vote_fields_response = {
        "status": 400,
        "error": "Invalid user input data (Voting fields).  Expected fields for 'candidate_id', 'office_name' and 'party_name'. Please try again."
    }

    party_id_cannot_be_zero_response = {
        "status": 400,
        "error": "Party ID cannot be zero or negative. Please try again"
    }

    party_id_out_of_range_response = {
        "status": 404,
        "error": "Party ID requested not in server. ID out of range."
    }

    office_id_out_of_range_response = {
        "status": 404,
        "error": "Office ID requested not in server. ID out of range."
    }

    email_already_exists_response = {
        "status": 409,
        "error": "Signup conflict - Email provided is already registered with another account"
    }

    passport_already_exists_response = {
        "status": 409,
        "error": "Signup conflict - Passport photo URL provided is already in use by another account"
    }

    telephone_already_exists_response = {
        "status": 409,
        "error": "Signup conflict - Telephone number provided is already in use by another account"
    }

    party_logo_already_exists_response = {
        "status": 409,
        "error": "Party registration conflict - Logo provided is already registered with another party"
    }

    party_hq_already_exists_response = {
        "status": 409,
        "error": "Party registration conflict - Address provided is already registered with another party"
    }

    party_name_already_exists_response = {
        "status": 409,
        "error": "Party registration conflict - Party name provided is already registered with another party"
    }

    office_already_exists_response = {
        "status": 409,
        "error": "Office registration conflict - Office name provided is already registered"
    }

    empty_data_field_response = {
        "status": 422,
        "error": "Empty data field detected. User input cannot be an empty string"
    }

    unknown_signup_data_field_response = {
        "status": 422,
        "error": "Unprocessable Entity - Invalid user input data (Signup data fields). Expected fields for 'first_name', 'last_name', 'other_name', 'email', 'telephone', 'passport_url', 'password' and 'confirm_password'. Please try again."
    }

    unknown_party_creation_data_field_response = {
        "status": 422,
        "error": "Unprocessable Entity - Invalid user input data (Party creation data fields). Expected fields for 'name', 'hq_address' and 'logo_url' . Please try again."
    }

    unknown_office_creation_data_field_response = {
        "status": 422,
        "error": "Unprocessable Entity - Invalid user input data (Office creation data fields). Expected fields for 'name' and 'type'. Please try again."
    }

    unknown_party_response = {
        "status": 422,
        "error": "Candidate Registration Failed. Party name provided is not registered. Please try again."
    }

    unknown_user_response = {
        "status": 422,
        "error": "Candidate Registration Failed.  User email provided is not registered. Please try again."
    }

    unexpected_data_types_resp = {
        "status": 422,
        "error": "Unexpected data type detected in user input. Expected strings only"
    }

    invalid_email_syntax_resp = {
        "status": 422,
        "error": "Invalid Email Syntax. Please correct email syntax and try again."
    }
    invalid_password_length_resp = {
        "status": 422,
        "error": "Invalid Password Length. 6 Characters minimum. Please adjust and try again"
    }

    invalid_office_types_resp = {
        "status": 422,
        "error": "Invalid Office types. Expected 'Federal', 'Legislative', 'State' or 'Local Government'. Please adjust and try again"
    }

    invalid_cadidate_id_resp = {
        "status": 422,
        "error": "Voting Error. Candididate ID provided is not registered. Please adjust and try again"
    }

    invalid_party_name_resp = {
        "status": 422,
        "error": "Voting Error. Party name provided is not registered. Please adjust and try again"
    }

    invalid_office_name_resp = {
        "status": 422,
        "error": "Voting Error. Office name provided is not registered. Please adjust and try again"
    }

    more_data_fields_response = {
        "status": 400, "error": "Bad Query - More data fields than expected"
    }
    unkown_fields_response = {
        "status": 400, "error": "Bad Query - Unexpected fields."
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
        "status": 404, "error": "Entity not in server. ID out of range."
    }

    mismatched_email_resp = {
        "status": 422,
        "error": "Passwords do not match"
    }
    unprocessable_data_response = {
        "status": 422,
        "error": "Unprocessable Entity - Invalid value in data field"
    }

    unprocessable_user_response = {
        "status": 422,
        "error": "Unprocessable Entity - User does not exist"
    }

    unprocessable_party_response = {
        "status": 422,
        "error": "Unprocessable Entity - Political party does not exist"
    }

    unprocessable_office_response = {
        "status": 422,
        "error": "Unprocessable Entity - Office type does not exist"
    }

    unprocessable_data_type_response = {
        "status": 422,
        "error": "Unprocessable Entity - Expected integers only"
    }

    @staticmethod
    def check_for_expected_keys_in_user_input(raw_data, expected_party_fields):
        """ (dict, list) -> bool
            Check for the expected fields in user_input.
            Return True/False
        """
        payload_list = list(raw_data.keys())
        return all(_ in expected_party_fields for _ in payload_list)

    @staticmethod
    def check_for_empty_strings_in_user_input(raw_data):
        """
            Checks for empty strings in user data
            Returns True/False
        """
        items_list = list(raw_data.values())
        return any(item.strip() == "" for item in items_list)

    @staticmethod
    def check_for_expected_value_types_in_user_input(raw_data):
        """ (dict) -> bool
            Check for expected value types
            return True/False
        """
        values_list = list(raw_data.values())
        return all(isinstance(item, str) for item in values_list)

    @staticmethod
    def check_valid_email_syntax(email):
        """
            Valdate email address
            Source: https://pythonspot.com/regular-expressions/
        """
        return re.match(r'[^@]+@[^@]+\.[^@]+', email)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            payload = jwt.decode(
                token, current_app.config.get('SECRET'), algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired has token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token detected. Please register or login"

    @staticmethod
    def check_list_contains_only_integers(the_list):
        """ Return true if all items are integers"""
        return all(isinstance(item, int) for item in the_list)

    @staticmethod
    def check_list_contains_only_positive_integers(the_list):
        """ Return true if all items are integers"""
        return all(item > 0 for item in the_list)
