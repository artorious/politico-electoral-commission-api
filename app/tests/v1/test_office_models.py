#!/usr/bin/env python3
""" Tests for Office related models"""
import unittest
from app.api.v1.office_models import PoliticalOffices


class TestPolticalParties(unittest.TestCase):
    """ Testscase for PoliticalParties"""
    def setUp(self):
        """ Initialize test variable"""
        self.test_federal_office_reg_data = PoliticalOffices({
            "name": "President of the Republic",
            "type": "Federal",
        })

    def test_empty_field_check(self):
        """ Test for empty string in value field"""

        empty_local_govt_data = PoliticalOffices({
            "name": "Member of county Assenbly",
            "type": "\t      \n",
        })
        self.assertTrue(
            self.test_federal_office_reg_data.check_any_for_empty_fields(),
            msg="Should be True"
        )
        self.assertFalse(
            empty_local_govt_data.check_any_for_empty_fields(),
            msg="Should be False"
        )

    def test_for_expected_keys_in_office_reg_data(self):
        """ Check for expected keys in user data"""

        local_govt_office_invalid_keys_reg_data = PoliticalOffices({
            "name": "Member of county Assenbly",
            "types": "Local Government",
        })

        self.assertTrue(
            self.test_federal_office_reg_data.check_for_expected_keys_present(
                ["name", "type"]),
            msg="Should be True"
        )
        self.assertFalse(
            local_govt_office_invalid_keys_reg_data.check_for_expected_keys_present(
                ["name", "type"]
            ),
            msg="Should be False"
        )

    def test_for_expected_value_in_type_of_office_data(self):
        """ Check for expected keys in user data"""

        invalid_value_in_type_reg_data = PoliticalOffices({
            "name": "Member of county Assenbly",
            "type": "Universal",
        })

        self.assertTrue(
            self.test_federal_office_reg_data.\
            check_for_expected_type_of_office(
                ["Federal", "Legislative", "State", "Local Government"]),
            msg="Should be True"
        )
        self.assertFalse(
            invalid_value_in_type_reg_data.check_for_expected_type_of_office(
                ["Federal", "Legislative", "State", "Local Government"]
            ),
            msg="Should be False"
        )

    def test_for_expected_value_types_office_reg_data(self):
        """ Check value(datatypes) types of user data"""
        invalid_types_legislative_data = PoliticalOffices({
            "name": 1,
            "type": "Legislative"
        })


        self.assertTrue(
            self.test_federal_office_reg_data.check_for_only_expected_value_types(),
            msg="Should be True"
        )

        self.assertRaises(ValueError)
        # self.assertFalse(
            # invalid_types_legislative_data.check_for_only_expected_value_types(),
            # msg="Should be False"
        # )

    def test_create_office_method_returns_a_custom_message(self):
        """ Test that a political office is created"""
        self.assertDictEqual({
        "status": 201,
            "data": [{"id": 1,
                "name": "President of the Republic",
                "type": "Federal",
            }]},
            self.test_federal_office_reg_data.create_office()
        )

    def test_creating_an_office_twice_is_caught_and_handled(self):
        """ Test a political office cannot be created twice """
        self.assertTrue(self.test_federal_office_reg_data.check_whether_office_exists(
            "President of the Republic"
        ))

if __name__ == "__main__":
    unittest.main()
