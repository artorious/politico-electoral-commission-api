#!/usr/bin/env python3
""" Tests for models"""
import unittest
from app.api.v1.models.party_models import PoliticalParties


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
            {'status': 201, 'data': [{'id': 1, 'name': 'Jubilee'}]},
            self.test_data.create_party()
        )

    def test_creating_a_party_twice_is_caught_and_handled(self):
        """ Test a political pary cannot be created twice """
        self.assertTrue(self.test_data.check_whether_party_exists("Jubilee"))

    def test_fetching_all_parties_returns_data(self):
        """ Test that a dictionary holding the data is returned """
        self.assertIsInstance(self.test_data.get_all_parties(), dict)

    def test_that_id_look_up_is_done_before_fetching(self):
        """ Test that method checks that the id value exists"""
        self.assertFalse(self.test_data.check_id_exists(1000000000000))

    def test_fetching_a_party_by_id_returns_data(self):
        """ Test method returns data"""
        self.assertIsInstance(self.test_data.fetch_a_party(1), list)

    def test_edit_party_performs_operation_and_returns_message(self):
        """ Test that valid user data gets updated """
        valid_update_data = {"name": "Ford Asili"}
        self.test_data.create_party()
        self.assertEqual(
            [{"id": 1, "name": "Ford Asili"}],
            PoliticalParties.edit_party(valid_update_data, 1),
            msg="Expected Success status and new name")

    def test_delete_party_opertaion_and_return_message(self):
        """ Tests atha operation returns message to user"""
        self.test_data.create_party()
        self.assertEqual(
            {'status': 200, 'data': [{'message': 'Party No. 1 deleted succesfully'}]},
            PoliticalParties.delete_party(1),
            msg="Expected Success status and new name")

if __name__ == "__main__":
    unittest.main()
