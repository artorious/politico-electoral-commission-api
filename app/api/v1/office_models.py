#!/usr/bin/env python3
""" Models Office Information """
import time

POLITICAL_OFFICES = []
OFFICE_COUNT = 1

class PoliticalOffices:
    def __init__(self, office_reg_data):
        self.office_reg_data = office_reg_data

    def create_office(self):
        """ Creates a political office"""
        pass

    def check_for_expected_keys_present(self, list_of_expected_keys):
        """ Checks for the expected keys in user input"""
        pass

    def check_for_expected_type_of_office(self, list_of_expected_types):
        """ Checks for the expected values in the type key in user input"""
        pass

    def check_any_for_empty_fields(self):
        """ Returns True only if the expected values in office registration
            details are not empty strings, else False
        """
        pass

    def check_for_only_expected_value_types(self):
        """ Returns True only if the expected value types in office registration
            details, else False
        """
        pass

    @staticmethod
    def check_whether_office_exists(office_name):
        """ Returns True if the office exists, else False"""
        pass

    @staticmethod
    def check_for_valid_office_name(name):
        """ Returns true if name is not space, empty, or less than 1 character
            else, returns False
        """
        pass



