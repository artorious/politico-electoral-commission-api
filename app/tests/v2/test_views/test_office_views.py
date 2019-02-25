#!/usr/bin/env python3
""" Test Cases for office Views/Routes """
import os
import unittest
import json
from app import create_app
from app.api.v2.models.database_models import DatabaseManager

class TestOfficeRoutes(unittest.TestCase):
    """ Parent test case for all office related views """

    def setUp(self):
        """ Initialize app and test variables """
        self.app = create_app(config_mode="testing")
        with self.app.app_context():
            self.client = self.app.test_client

            self.federal_office_reg_data = {
                "name": "President of the Republic",
                "type": "Federal"
            }
            self.legislative_office_reg_data = {
                "name": "Member of Congress",
                "type": "Legislative"
            }
            self.state_office_reg_data = {
                "name": "Governor",
                "type": "State"
            }
            self.local_govt_office_reg_data = {
                "name": "Member of county Assenbly",
                "type": "Local Government"
            }


            self.admin_login_data = {
                "email": os.getenv("ADMIN_EMAIL"), "password": os.getenv("DEFAULT_RAW_ADMIN_PASS")}
            login_results = self.client().post("/api/v2/auth/login", data=json.dumps(self.admin_login_data))
            auth_token = json.loads(login_results.data)["message"][0]["token"]
            self.updated_header = {"content-type": "application/json", "Authorization": f"Bearer {auth_token}"}


    def tearDown(self):
        with self.app.app_context():
            db = DatabaseManager()
            db.drop_tables()



class TestOfficeCreation(TestOfficeRoutes):
    """ Tests for creating a political party """

    def test_office_creation_with_valid_data(self):
        """ Test office creation with valid data """
        response = self.client().post(
            "/api/v2/offices",
            data=json.dumps(self.federal_office_reg_data),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertIn("office", deserialized_response)

        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (created)"
        )


    def test_office_creation_with_more_fields_than_is_expected(self):
        """ Test with more fields than expected. """
        test_extra_data = {
            "name": "Member of Congress",
            "type": "Legislative",
            "sneak": "I'm not supposed to be here"
        }

        response = self.client().post(
            "/api/v2/offices",
            data=json.dumps(test_extra_data),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 400,
            msg="response code SHOULD BE 400 (bad query)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Invalid user input data (Office creation data fields). Expected fields for 'name' and 'type'. Please try again.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_office_creation_with_fewer_fields_than_expected(self):
        """ Test with fewer fields than expected """
        test_insufficient_data = {"name": "Member of Congress"}

        response = self.client().post(
            "/api/v2/offices",
            data=json.dumps(test_insufficient_data),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 400,
            msg="response code SHOULD BE 400 (bad query)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Invalid user input data (Office creation data fields). Expected fields for 'name' and 'type'. Please try again.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_office_creation_with_an_empty_string_in_field(self):
        """ Test with an empty string in field """
        empty_governer_data = {
            "name": "",
            "type": "State",
        }
        empty_local_govt_data = {
            "name": "Member of county Assenbly",
                   "type": "\t      \n",
        }

        response = self.client().post(
            "/api/v2/offices",
            data=json.dumps(empty_governer_data),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422 (Unprocessable Entity)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Empty data field detected. User input cannot be an empty string",
            msg="Response Body Contents- Should be custom message "
        )

        response = self.client().post(
            "/api/v2/offices",
            data=json.dumps(empty_local_govt_data),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422 (Unprocessable Entity) "
        )
        self.assertEqual(
            deserialized_response["error"],
            "Empty data field detected. User input cannot be an empty string",
            msg="Response Body Contents- Should be custom message "
        )

    def test_office_creation_with_already_existing_posting(self):
        """ Test that a office posting cannot be created twice """
        response = self.client().post(
            "/api/v2/offices",
            data=json.dumps(self.legislative_office_reg_data),
            headers=self.updated_header
        )

        response = self.client().post(
            "/api/v2/offices",
            data=json.dumps(self.legislative_office_reg_data),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 409,
            msg="response code SHOULD BE 409 (Conflict)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Office registration conflict - Office name provided is already registered",
            msg="Response Body Contents- Should be custom message "
        )


class TestFetchingOffice(TestOfficeRoutes):
    """ Test for feching a single political office by ID """
    def test_fetching_of_created_offices(self):
        """ Test succesful fetch of all messages """
        response = self.client().get("/api/v2/offices", headers=self.updated_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", str(response.data))
        self.assertIn("status", str(response.data))

    def test_fetching_an_office_by_id_with_a_valid_and_existing_id(self):
        """ Test the fetching of a single pilitical office using it's id """
        response = self.client().post(
            "/api/v2/offices",
            data=json.dumps(self.federal_office_reg_data),
            headers=self.updated_header
        )

        response = self.client().get('/api/v2/offices/1', headers=self.updated_header)
        self.assertEqual(response.status_code, 200, msg="Should be 200(ok)")
        self.assertIn("status", str(response.data))

    def test_fetching_an_office_with_a_negative_id_value(self):
        """ Test with a negative integer """
        response = self.client().get("/api/v2/offices/-1", headers=self.updated_header)
        deserialized_response = json.loads(response.data.decode())

        self.assertEqual(
            response.status_code, 404, msg="Should be 404 - (Not found)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Resource not found on the server.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_fetching_an_office_with_a_valid_id_that_is_out_of_bound(self):
        """ Test with a integer that is out of bound (416 - Out of range)"""

        response = self.client().get("/api/v2/offices/1000", headers=self.updated_header)
        deserialized_response = json.loads(response.data.decode())

        self.assertEqual(
            response.status_code, 416, msg="Should be 416 - Out of range"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Entity not in server. ID out of range.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_fetching_an_office_with_a_floating_point_value_for_id(self):
        """ Test with a floating point number """
        response = self.client().get("/api/v2/offices/1.0", headers=self.updated_header)
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

    def test_fetching_an_office_with_a_non_numeric_value_for_id(self):
        """ Test fetching with a non-numeric character 404 Not found """
        response = self.client().get("/api/v2/office/one", headers=self.updated_header)
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

    def test_fetching_an_office_without_providing_a_value_blank_field(self):
        """ 400 - Bad query"""
        response = self.client().get("/api/v2/offices/", headers=self.updated_header)
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
