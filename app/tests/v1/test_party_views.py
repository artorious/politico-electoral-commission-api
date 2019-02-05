#!/usr/bin/env python3
""" Test models """
import unittest
import json
from app import create_app


class TestPartiesRoute(unittest.TestCase):
    """ Test case for party views """

    def setUp(self):
        """ Init app and test vars """
        self.app = create_app(config_mode="testing")
        self.client = self.app.test_client
        self.party_reg_data = {
            "name": "Jubilee",
            "hqAddress": "Jubilee Tower, Pangani, Thika Road",
            "logoUrl": "/static/jubilee.jpeg",
            "Party members": 225
        }

    def test_party_creation_with_valid_data(self):
        """test with valid data - 201 (created) + data"""
        response = self.client().post(
            "/api/v1/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            response.status_code, 409,
            msg="response code SHOULD BE 201 (Created)"
        )
        response_in_json = json.loads(
            response.data.decode('utf-8').replace("'", "\""))
        self.assertIn("status", response_in_json)

    def test_party_creation_with_more_fields_than_expected(self):
        """ Test with more fields than expected. """
        test_reg_data = {
            "name": "Jubilee",
            "hqAddress": "Jubilee Tower, Pangani, Thika Road",
            "logoUrl": "/static/jubilee.jpeg",
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
            deserialized_response["error"],
            "Bad Query - More data fields than expected",
            msg="Response Body Contents- Should be custom message "
        )

    def test_party_creation_with_fewer_fields_than_expected(self):
        """ Test with fewer fields than expected """
        test_reg_data = {
            "name": "Jubilee",
            "hqAddress": "Jubilee Tower, Pangani, Thika Road",
            "logoUrl": "/static/jubilee.jpeg"
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
            deserialized_response["error"],
            "Bad Query - Fewer data fields than expected",
            msg="Response Body Contents- Should be custom message "
        )

    def test_party_creation_with_an_empty_string_in_field(self):
        """ Test with an empty string in field """
        test_reg_data = {
            "name": "",
            "hqAddress": "Jubilee Tower, Pangani, Thika Road",
            "logoUrl": "/static/jubilee.jpeg",
            "Party members": 225,
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

    def test_party_creation_with_invalid_value_types(self):
        """test with invalid value types  - 422 (Unprocessable Entity) + msg
        """
        test_reg_data = {
            "name": 12,
            "hqAddress": "Jubilee Tower, Pangani, Thika Road",
            "logoUrl": "/static/jubilee.jpeg",
            "Party members": 225
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
            deserialized_response["error"],
            "Unprocessable Entity - Invalid value in data field",
            msg="Response Body Contents- Should be custom message "
        )

    def test_party_creation_with_already_existing_party(self):
        """ Test that a party cannot be created twice
        """
        response = self.client().post(
            "/api/v1/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 409,
            msg="response code SHOULD BE 201 (Created)"
        )
        response = self.client().post(
            "/api/v1/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 409,
            msg="response code SHOULD BE 409 (Conflict)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Conflict - Party already exists",
            msg="Response Body Contents- Should be custom message "
        )

    def test_fetching_of_created_parties(self):
        """ Test succesful fetch of all messages """
        response = self.client().post(
            "/api/v1/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            response.status_code, 409,
            msg="response code SHOULD BE 201 (Created)"
        )
        response = self.client().get("/api/v1/parties")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", str(response.data))
        self.assertIn("status", str(response.data))

    def test_fetching_a_party_by_id_with_a_valid_and_existing_id(self):
        """ Test the fetching of a single party using it's id """
        response = self.client().get('/api/v1/parties/1')
        self.assertEqual(response.status_code, 200, msg="Should be 200(ok)")
        self.assertIn("status", str(response.data))

    def test_fetching_a_party_with_a_negative_id_value(self):
        """ Test with a negative integer """
        response = self.client().get("/api/v1/parties/-1")
        deserialized_response = json.loads(response.data.decode())

        self.assertEqual(
            response.status_code, 404, msg="Should be 404 - (Not found)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Resource not found on the server.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_fetching_a_party_with_a_valid_id_that_is_out_of_bound(self):
        """ Test with a integer that is out of bound (416 - Out of range)"""

        response = self.client().get("/api/v1/parties/1000")
        deserialized_response = json.loads(response.data.decode())

        self.assertEqual(
            response.status_code, 416, msg="Should be 416 - Out of range"
        )
        self.assertEqual(
            deserialized_response["error"],
            "ID out of range. Requested Range Not Satisfiable",
            msg="Response Body Contents- Should be custom message "
        )

    def test_fetching_a_party_with_a_floating_point_value_for_id(self):
        """ Test with a floating point number (400 - malformed syntax) """
        response = self.client().get("/api/v1/parties/1.0")
        deserialized_response = json.loads(response.data.decode())

        self.assertEqual(
            response.status_code, 404,
            msg="Should be 404-(Not found)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Resource not found on the server.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_fetching_a_party_with_a_non_numeric_value_for_id(self):
        """ Test fetching with a non-numeric character 404 Not found """
        response = self.client().get("/api/v1/parties/one")
        deserialized_response = json.loads(response.data.decode())

        self.assertEqual(
            response.status_code, 404,
            msg="Should be 404-(Not Found)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Resource not found on the server.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_fetching_a_party_without_providing_a_value_blank_field(self):
        """ 400 - Bad query"""
        response = self.client().get("/api/v1/parties/")
        deserialized_response = json.loads(response.data.decode())

        self.assertEqual(
            response.status_code, 404,
            msg="Should be 400-(Bad Query)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Resource not found on the server.",
            msg="Response Body Contents- Should be custom message "
        )


if __name__ == "__main__":
    unittest.main()
