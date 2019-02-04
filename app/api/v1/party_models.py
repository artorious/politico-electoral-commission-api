#!/usr/bin/env python3
""" Data representation - Routines for user to interact with the API. """

import datetime

political_parties = []
party_count = 1

class PoliticalParties:

    def __init__(self, party_reg_details):
        self.party_reg_details = party_reg_details
        self.errors = []

    def create_party(self):
        """ Validate, append, return custom message """
        # TODO:
        if self.errors == []:
            pass
        else:
            pass

    def check_for_expected_keys(self, list_of_expected_keys):
        """ (dict, list) -> bool
            Checks for dict-key equality
        """
        pass

    
    def check_for_any_empty_fields(self):
        """ (dict) -> bool
            checks for empty strings 
        """
        pass

    

    def check_for_expected_value_types(self):
        """ Check for expected value types"""
        pass
       

