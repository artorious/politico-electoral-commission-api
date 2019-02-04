#!/usr/bin/env python3
import unittest
from app.api.v1.party_models import PoliticalParties


class TestPolticalParties(unittest.TestCase):
    def setUp(self):
        self.test_data = PoliticalParties({
            "name" : "Jubilee" ,
            "hqAddress" : "Jubilee Tower, Pangani, Thika Road" ,
            "logoUrl" : "/static/jubilee.jpeg" ,
            "Party members": 225
        })
    
    def test_empty_field_check(self):
        empty_str = PoliticalParties({
            "name" : "" ,
            "hqAddress" : "Jubilee Tower, Pangani, Thika Road" ,
            "logoUrl" : "/static/jubilee.jpeg" ,
            "Party members": 225
        })
        self.assertTrue(self.test_data.check_for_any_empty_fields, msg="Should be True")
        self.assertEqual(empty_str.check_for_any_empty_fields, "Empty data field")
    
    def test_expected_keys_check(self):
        test_data2 = PoliticalParties({
            "names" : "jubilee" ,
            "hqAddress" : "Jubilee Tower, Pangani, Thika Road" ,
            "logoUrl" : "/static/jubilee.jpeg" ,
            "Party members": 225
        })
        self.assertTrue(self.test_data.check_for_expected_keys, msg="Should be True")
        self.assertEqual(test_data2.check_for_expected_keys, "Unrecognized data field")

    def test_expected_value_types(self):
        wrong_value_types = PoliticalParties({ 
            "name" : 12 ,
            "hqAddress" : "Jubilee Tower, Pangani, Thika Road" ,
            "logoUrl" : "/static/jubilee.jpeg" ,
            "Party members": 225,
            "nickname": "I'm not supposed to be here"
        })
        self.assertTrue(self.test_data.check_for_expected_value_types, msg="Should be True")
        self.assertEqual(wrong_value_types.check_for_expected_value_types, "Invalid value in data field")
    
    def test_create_party_return_msg(self):
        self.assertDictEqual({"id" : 1 , "name" : "Jubilee"}, self.test_data.create_party)
    
    def test_creating_a_party_twice(self):
        self.test_data.create_party()
        self.assertEqual(self.test_data.create_party(), "Party already exists")


if __name__ == "__main__":
    unittest.main()