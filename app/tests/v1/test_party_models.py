#!/usr/bin/env python3
""" Tests for models"""
import unittest
from app.api.v1.party_models import PoliticalParties


class TestPolticalParties(unittest.TestCase):
    """ Testscase for PoliticalParties"""
    def setUp(self):
        """ Init test variable"""
        self.test_data = PoliticalParties({
            "name": "Jubilee",
            "hqAddress": "Jubilee Tower, Pangani, Thika Road",
            "logoUrl": "/static/jubilee.jpeg",
            "Party members": 225
        })

    def test_empty_field_check(self):
        """ Test for empty string in value field"""
        empty_str = PoliticalParties({
            "name": "",
            "hqAddress": "Jubilee Tower, Pangani, Thika Road",
            "logoUrl": "/static/jubilee.jpeg",
            "Party members": 225
        })
        self.assertTrue(
            self.test_data.check_for_any_empty_fields(), msg="Should be True"
        )
        self.assertFalse(
            empty_str.check_for_any_empty_fields(), msg="Should be False"
        )

    def test_expected_keys_in_party_reg_data_check(self):
        """ Check for expected keys in user data"""
        test_data2 = PoliticalParties({
            "names": "jubilee",
            "hqAddress": "Jubilee Tower, Pangani, Thika Road",
            "logoUrl": "/static/jubilee.jpeg",
            "Party members": 225
        })
        self.assertTrue(
            self.test_data.check_for_expected_keys(
                ["name", "hqAddress", "logoUrl", "Party members"]),
            msg="Should be True"
        )
        self.assertFalse(
            test_data2.check_for_expected_keys(
                ["name", "hqAddress", "logoUrl", "Party members"]
            ),
            msg="Should be False"
        )

    def test_expected_value_types_party_reg_data(self):
        """ Check value(datatypes) types of user data"""
        wrong_value_types = PoliticalParties({
            "name": 12,
            "hqAddress": "Jubilee Tower, Pangani, Thika Road",
            "logoUrl": "/static/jubilee.jpeg",
            "Party members": 225
        })
        self.assertTrue(
            self.test_data.check_for_expected_value_types(),
            msg="Should be True"
        )
        self.assertFalse(
            wrong_value_types.check_for_expected_value_types(),
            msg="Should be False"
        )

    def test_create_party_method_returns_a_custom_message(self):
        """ Test a political prty is created"""
        self.assertDictEqual(
            {'status': 'success', 'data': [{'id': 1, 'name': 'Jubilee'}]},
            self.test_data.create_party()
        )

    def test_creating_a_party_twice_is_caught_and_handled(self):
        """ Test a political pary cannot be created twice """
        self.test_data.create_party()
        self.assertDictEqual(
            self.test_data.create_party(),
            {'status': 'Failed', 'error': 'Party already exists'}
        )

    def test_fetching_all_parties_returns_data(self):
        """ Test that a dictionary holding the data is returned """
        self.assertIsInstance(self.test_data.get_all_parties(), dict)

    def test_that_id_look_up_is_done_before_fetching(self):
        """ Test that method checks that the id value exists"""
        # try ferching an obnoxious no.
        self.assertDictEqual(
            {"status": "Failed", "error": "String: relevant-error-message"},
            self.test_data.fetch_a_party(1000000),
            msg=" Expected error message"
        )

    def test_fetching_a_party_by_id_returns_data(self):
        """ Test method returns data"""
        self.assertIsInstance(self.test_data.fetch_a_party(1), dict)


if __name__ == "__main__":
    unittest.main()
