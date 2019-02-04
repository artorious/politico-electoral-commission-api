#!/usr/bin/env python3

import unittest
import os
import json
from app import create_app


class PartiesTestCase(unittest.TestCase):
    """ Test case for party views"""

    def setUp(self):
        """ Init app and test vars """
        self.app = create_app(config_mode="testing")
        self.client = self.app.test_client
        self.party_reg_data = { 
            "name" : "Jubilee" ,
            "hqAddress" : "Jubilee Tower, Pangani, Thika Road" ,
            "logoUrl" : "/static/jubilee.jpeg" ,
            "Party members": 225
        }
   
    def test_party_creation_with_valid_data(self):
        """test with valid data - 201 (created) + data"""
        response = self.client().post(
            "/api/v1/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'} 
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (Created)"
        )
        self.assertEqual(
            deserialized_response["data"], 
            {"id" : 1 , "name" : "Jubilee"},
            msg="Response Body Contents- Should be party name and id "
        )


    def test_with_non_json_data(self):
        """test with invalid json - 415 (Unsupported Media Type) + msg"""
        test_reg_data = b'Jubilee'

        response = self.client().post(
            "/api/v1/parties",
            data=json.dumps(test_reg_data),
            headers={'content-type': 'application/json'} 
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 415,
            msg="response code SHOULD BE 415 (Unsupported Media Type)"
        )
        self.assertEqual(
            deserialized_response["error"], "Expected JSON content only.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_with_more_fields_than_expected(self):
        """
        test with more fields than expected - 400 (Malformed syntax or a bad query) + msg
        """
        test_reg_data = { 
            "name" : "Jubilee" ,
            "hqAddress" : "Jubilee Tower, Pangani, Thika Road" ,
            "logoUrl" : "/static/jubilee.jpeg" ,
            "Party members": 225,
            "nickname": "I'm not supposed to be here"
        }

        response = self.client().post(
            "/api/v1/parties",
            data=json.dumps(test_reg_data),
            headers={'content-type': 'application/json'} 
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 400,
            msg="response code SHOULD BE 400 (bad query) + msg"
        )
        self.assertEqual(
            deserialized_response["error"], "More data fields than expected",
            msg="Response Body Contents- Should be custom message "
        )

    def test_with_fewer_fields_than_expected(self):
        """ 
        test with fewer fields than expected - 400 (Malformed syntax or a bad query) + msg
        """
        test_reg_data = { 
            "name" : "Jubilee" ,
            "hqAddress" : "Jubilee Tower, Pangani, Thika Road" ,
            "logoUrl" : "/static/jubilee.jpeg"
        }

        response = self.client().post(
            "/api/v1/parties",
            data=json.dumps(test_reg_data),
            headers={'content-type': 'application/json'} 
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 400,
            msg="response code SHOULD BE 400 (bad query) + msg"
        )
        self.assertEqual(
            deserialized_response["error"], "Fewer data fields than expected",
            msg="Response Body Contents- Should be custom message "
        )
    
    def test_with_worngly_name_field_from_expected(self):
        """
        test with a wrongly named field from expected - 400 (Malformed syntax or a bad query) + msg
        """
        test_reg_data = { 
            "names" : "Jubilee" ,
            "hqAddress" : "Jubilee Tower, Pangani, Thika Road" ,
            "logoUrl" : "/static/jubilee.jpeg" ,
            "Party members": 225,
            "nickname": "I'm not supposed to be here"
        }

        response = self.client().post(
            "/api/v1/parties",
            data=json.dumps(test_reg_data),
            headers={'content-type': 'application/json'} 
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 400,
            msg="response code SHOULD BE 400 (malformed syntax) + msg"
        )
        self.assertEqual(
            deserialized_response["error"], "Unrecognized data field",
            msg="Response Body Contents- Should be custom message "
        )

    def test_with_an_empty_string_in_field(self):
        """
        test with an empty str - 422 (Unprocessable Entity) + msg
        """
        test_reg_data = { 
            "name" : "" ,
            "hqAddress" : "Jubilee Tower, Pangani, Thika Road" ,
            "logoUrl" : "/static/jubilee.jpeg" ,
            "Party members": 225,
            "nickname": "I'm not supposed to be here"
        }

        response = self.client().post(
            "/api/v1/parties",
            data=json.dumps(test_reg_data),
            headers={'content-type': 'application/json'} 
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422 (Unprocessable Entity) + msg"
        )
        self.assertEqual(
            deserialized_response["error"], "Empty data field",
            msg="Response Body Contents- Should be custom message "
        )

    def test_with_invalid_value_types(self):
        """test with invalid value types  - 422 (Unprocessable Entity) + msg
        """
        test_reg_data = { 
            "name" : 12 ,
            "hqAddress" : "Jubilee Tower, Pangani, Thika Road" ,
            "logoUrl" : "/static/jubilee.jpeg" ,
            "Party members": 225,
            "nickname": "I'm not supposed to be here"
        }

        response = self.client().post(
            "/api/v1/parties",
            data=json.dumps(test_reg_data),
            headers={'content-type': 'application/json'} 
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422 (Unprocessable Entity) + msg"
        )
        self.assertEqual(
            deserialized_response["error"], "Invalid value in data field",
            msg="Response Body Contents- Should be custom message "
        )

    def test_with_already_created_party(self):
        """ Test that a party cannot be created twice
        202 (Accepted)
        """
        response = self.client().post(
            "/api/v1/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'} 
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (Created)"
        )
        response_2 = self.client().post(
            "/api/v1/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'} 
        )
        deserialized_response = json.loads(response_2.data.decode())
        self.assertEqual(
            response_2.status_code, 202,
            msg="response code SHOULD BE 202 (Accepted)"
        )
        self.assertEqual(
            deserialized_response["error"], "Party already exists",
            msg="Response Body Contents- Should be custom message "
        )

if __name__ == "__main__":
    unittest.main()

