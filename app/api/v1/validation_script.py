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



class ValidationHelper:

    def check_whether_entity_exists(self, entity_name, entity_list):
        """ Returns True if the office exists, else False"""
        entity_already_present = False
        for each_entity in entity_list:
            if each_entity["name"] == entity_name:
                entity_already_present = True

        return entity_already_present
