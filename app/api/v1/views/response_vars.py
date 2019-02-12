#!/usr/bin/env python3
""" Validates user input to interact with the API. """

more_data_fields_response = {
    "status": 400,
    "error": "Bad Query - More data fields than expected"
}

few_data_fields_response = {
    "status": 400,
    "error": "Bad Query - Fewer data fields than expected"
}

id_cannot_be_zero_response = {
    "status": 400,
    "error": "ID cannot be zero or negative"
}

entity_already_exists_response = {
    "status": 409,
    "error": "Conflict - Entity already exists"
}

id_out_of_range_response = {
    "status": 416,
    "error": "Entity not in server. ID out of range."
}

unprocessable_data_response = {
    "status": 422,
    "error": "Unprocessable Entity - Invalid value in data field"
}

empty_data_field_response = {
    "status": 422,
    "error": "Empty data field"
}

expected_offices = ["Federal", "Legislative", "State", "Local Government"]

expected_party_fields = ["name", "hqAddress", "logoUrl", "Party members"]

expected_office_fields = ["name", "type"]


