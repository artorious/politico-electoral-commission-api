#!/usr/bin/env python3
""" Holds Methods to Validate App data """
import re
import jwt
from flask import  current_app
from app.api.v2.models.database_models import DatabaseManager


class ValidationHelper(DatabaseManager):
    """ Methods that Validate user input"""
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
    party_already_exists_response = {
        "status": 409, "error": "Conflict - Party already exists"
    }
    email_already_exists_response = {
        "status": 409, "error": "Conflict - Email already in use"
    }
    logo_already_exists_response = {
        "status": 409, "error": "Conflict - Logo already in use"
    }
    passport_already_exists_response = {
        "status": 409, "error": "Conflict - Passport photo already in use"
    }
    hq_already_exists_response = {
        "status": 409, "error": "Conflict - Address already in use"
    }
    telephone_already_exists_response = {
        "status": 409, "error": "Conflict - Phone number already registered"
    }
    id_out_of_range_response = {
        "status": 404, "error": "Entity not in server. ID out of range."
    }
    unexpected_data_types_resp = {
        "status": 422,
        "error": "Unexpected data types. Expectes strings only"
    }
    invalid_password_length_resp = {
        "status": 422,
        "error": "Invalid Password Length. 6 Characters minimum"
    }
    invalid_email_syntax_resp = {
        "status": 422,
        "error": "Invalid Email Syntax"
    }
    mismatched_email_resp = {
        "status": 422,
        "error": "Passwords do not match"
    }
    unprocessable_data_response = {
        "status": 422,
        "error": "Unprocessable Entity - Invalid value in data field"
    }
    empty_data_field_response = {
        "status": 422, "error": "Empty data field"
    }

    @staticmethod
    def check_for_expected_keys_in_user_input(raw_data, expected_party_fields):
        """ (dict, list) -> bool
            Check for the expected fields in user_input.
            Return True/False
        """
        return list(raw_data.keys()) == expected_party_fields

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
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired has token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token detected. Please register or login"
