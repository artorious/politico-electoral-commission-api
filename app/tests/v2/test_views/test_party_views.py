#!/usr/bin/env python3
""" Test Cases for Views/Routes """
import unittest
import json
from app import create_app
from app.api.v2.models.database_models import DatabaseManager

class TestPartiesRoutes(unittest.TestCase):
    """ Parent test case for all party related views """

    def setUp(self):
        """ Init app and test vars """

        self.app = create_app(config_mode="testing")
        with self.app.app_context():
            self.client = self.app.test_client
            self.party_reg_data = {
                "name": "Jubilee",
                "hq_address": "Jubilee Tower, Pangani, Thika Road",
                "logo_url": "/static/jubilee.jpeg"
            }

    def tearDown(self):
        with self.app.app_context():
            db = DatabaseManager()
            db.drop_tables()


class TestPartyCreation(TestPartiesRoutes):
    """ Tests for creating a political party """
    def test_party_creation_with_valid_data(self):
        """test with valid data - 201 (created) + data"""
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )
        response_in_json = json.loads(
            response.data.decode('utf-8').replace("'", "\""))
        self.assertIn("status", response_in_json)

        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (created)"
        )

    def test_party_creation_with_more_fields_than_expected(self):
        """ Test with more fields than expected. """
        test_reg_data = {
            "name": "Jubilee",
            "hq_address": "Jubilee Tower, Pangani, Thika Road",
            "logo_url": "/static/jubilee.jpeg",
            "nickname": "I'm not supposed to be here"
        }

        response = self.client().post(
            "/api/v2/parties",
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
            "hq_address": "Jubilee Tower, Pangani, Thika Road"
        }

        response = self.client().post(
            "/api/v2/parties",
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
            "hq_address": "Jubilee Tower, Pangani, Thika Road",
            "logo_url": "/static/jubilee.jpeg",
        }
        test_reg_data1 = {
            "name": "Jubilee",
            "hq_address": "\t",
            "logo_url": "/static/jubilee.jpeg",
        }
        test_reg_data2 = {
            "name": "Jubilee",
            "hq_address": "Jubilee Tower, Pangani, Thika Road",
            "logo_url": "\n",
        }

        response = self.client().post(
            "/api/v2/parties",
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

        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(test_reg_data1),
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

        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(test_reg_data2),
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
            "hq_address": "Jubilee Tower, Pangani, Thika Road",
            "logo_url": "/static/jubilee.jpeg"
        }

        response = self.client().post(
            "/api/v2/parties",
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
            "/api/v2/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (Created)"
        )
        party_reg_data = {
                "name": "Jubilee",
                "hq_address": "None Tower, Pangani, Thika Road",
                "logo_url": "/static/jubilee1.jpeg"
            }
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(party_reg_data),
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
    def test_party_creation_with_already_existing_party_logo(self):
        """ Test that a party logo cannot be used twice
        """
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (Created)"
        )
        party_reg_data = {
                "name": "A party",
                "hq_address": "An Address",
                "logo_url": "/static/jubilee.jpeg"
            }
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(party_reg_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 409,
            msg="response code SHOULD BE 409 (Conflict)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Conflict - Logo already in use",
            msg="Response Body Contents- Should be custom message "
        )
    def test_party_creation_with_already_existing_party_hq(self):
        """ Test that a party headquarters cannot be registered twice
        """
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (Created)"
        )

        party_reg_data = {
                "name": "A party",
                "hq_address": "Jubilee Tower, Pangani, Thika Road",
                "logo_url": "url-goes-here"
            }
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(party_reg_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 409,
            msg="response code SHOULD BE 409 (Conflict)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Conflict - Address already in use",
            msg="Response Body Contents- Should be custom message "
        )




class TestFetchingParty(TestPartiesRoutes):
    """ Test for feching political parties """
    def test_fetching_of_created_parties(self):
        """ Test succesful fetch of all messages """
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (Created)"
        )
        response = self.client().get("/api/v2/parties")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Political Parties", str(response.data))
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
        """ Test with a integer that is out of Range"""

        response = self.client().get("/api/v2/parties/1000")
        deserialized_response = json.loads(response.data.decode())

        self.assertEqual(
            response.status_code, 404, msg="Should be 404"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Entity not in server. ID out of range.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_fetching_a_party_with_a_floating_point_value_for_id(self):
        """ Test with a floating point number """
        response = self.client().get("/api/v2/parties/1.0")
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
        response = self.client().get("/api/v2/parties/one")
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
        response = self.client().get("/api/v2/parties/")
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

class TestDeleteParty(TestPartiesRoutes):
    """ Test cases for deleting a party """

    def test_deleting_party_with_a_negative_id(self):
        """ Test deleting with a negative ID"""
        response = self.client().delete("/api/v2/parties/-1")
        deserialized_response = json.loads(response.data.decode())

        self.assertEqual(
            response.status_code, 404, msg="Should be 404 - (Not found)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Resource not found on the server.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_deleting_party_with_an_out_of_bound_id(self):
        """ Test with a integer that is out of range"""

        response = self.client().delete("/api/v2/parties/1000")
        deserialized_response = json.loads(response.data.decode())

        self.assertEqual(
            response.status_code, 404, msg="Should be 404"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Entity not in server. ID out of range.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_with_non_int_as_id(self):
        """ Try to delete with an ID that isnt an int """
        response = self.client().delete("/api/v2/parties/one")
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

    def test_test_with_float_as_id(self):
        """ Test Deleting with a floating point ID"""
        response = self.client().delete("/api/v2/parties/1.0")
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

class TestEditParty(TestPartiesRoutes):
    """ Test for editing a political party by ID """

    def test_edit_party_with_non_integer_id_and_valid_name(self):
        """ Test invalid type for party ID throws a 404 code """
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )

        valid_update_data = {"name": "Ford Asili"}
        response = self.client().patch(
            "/api/v2/parties/one/name",
            data=json.dumps(valid_update_data),
            headers={'content-type': 'application/json'}
        )
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

    def test_edit_party_with_an_out_of_range_id(self):
        """ Test with an ID that is out of range  """
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )

        valid_update_data = {"name": "Ford Asili"}
        response = self.client().patch(
            "/api/v2/parties/100000/name",
            data=json.dumps(valid_update_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 404, msg="Should be 404"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Entity not in server. ID out of range.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_edit_party_with_a_float_as_id(self):
        """ 404 """
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )

        valid_update_data = {"name": "Ford Asili"}
        response = self.client().patch(
            "/api/v2/parties/1.0/name",
            data=json.dumps(valid_update_data),
            headers={'content-type': 'application/json'}
        )

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

    def test_edit_party_with_negative_id(self):
        """ Test with a negative value for ID """
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )

        valid_update_data = {"name": "Ford Asili"}
        response = self.client().patch(
            "/api/v2/parties/-1/name",
            data=json.dumps(valid_update_data),
            headers={'content-type': 'application/json'}
        )

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


    def test_edit_party_with_with_valid_id_and_empty_name_field(self):
        """ 400 no paylaod"""
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )

        response = self.client().patch(
            "/api/v2/parties/1/name",
            headers={'content-type': 'application/json'}
        )

        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 400,
            msg="Should be 400-(Bad Query)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Malformed request syntax or invalid request message framing",
            msg="Response Body Contents- Should be custom message "
        )

    def test_edit_party_with_more_fields_than_expected(self):
        """ Test with more fields than Expected -400"""

        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )

        extra_update_data = {
            "name": "Ford Asili",
            "logoUrl": "/static/jubilee.jpeg"
        }
        response = self.client().patch(
            "/api/v2/parties/1/name",
            data=json.dumps(extra_update_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 400,
            msg="response code SHOULD BE 400 (bad query)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Bad Query - More data fields than expected",
            msg="Response Body Contents- Should be custom message "
        )

    def test_edit_party_with_id_value_zero(self):
        """ Test with a zero as value for ID """
        response = self.client().post(
            "/api/v2/parties",
            data=json.dumps(self.party_reg_data),
            headers={'content-type': 'application/json'}
        )

        valid_update_data = {"name": "Ford Asili"}
        response = self.client().patch(
            "/api/v2/parties/0/name",
            data=json.dumps(valid_update_data),
            headers={'content-type': 'application/json'}
        )

        deserialized_response = json.loads(response.data.decode())

        self.assertEqual(
            response.status_code, 400,
            msg="Should be 400 status"
        )
        self.assertEqual(
            deserialized_response["error"],
            'ID cannot be zero or negative',
            msg="Response Body Contents- Should be custom message "
        )

