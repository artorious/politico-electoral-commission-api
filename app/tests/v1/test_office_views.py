#!/usr/bin/env python3
""" Test Cases for office Views/Routes """
import unittest
import json
from app import create_app


class TestOfficeRoutes(unittest.TestCase):
    """ Parent test case for all office related views """

    def setUp(self):
        """ Initialize app and test variables """
        self.app = create_app(config_mode="testing")
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
            "type": "State",
        }
        self.local_govt_office_reg_data = {
            "name": "Member of county Assenbly",
            "type": "Local Government"
        }



class TestOfficeCreation(TestOfficeRoutes):
    """ Tests for creating a political party """
    def test_office_creation_with_valid_data(self):
        """ Test office creation with valid data """
        response = self.client().post(
            "/api/v1/offices",
            data=json.dumps(self.federal_office_reg_data),
            headers={'content-type': 'application/json'}
        )
        response_in_json = json.loads(
            response.data.decode('utf-8').replace("'", "\""))
        self.assertIn("status", response_in_json)

    def test_ofice_creation_with_more_fields_than_is_expected(self):
        """ Test with more fields than expected. """
        test_extra_data =legislative_office_reg_data = {
            "name": "Member of Congress",
            "type": "Legislative",
            "sneak": "I'm not supposed to be here"
        }


        response = self.client().post(
            "/api/v1/offices",
            data=json.dumps(test_extra_data),
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

    def test_office_creation_with_fewer_fields_than_expected(self):
        """ Test with fewer fields than expected """
        test_insufficient_data = {"name": "Member of Congress"}

        response = self.client().post(
            "/api/v1/offices",
            data=json.dumps(test_insufficient_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 400,
            msg="response code SHOULD BE 400 (bad query)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Bad Query - Fewer data fields than expected",
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
            "/api/v1/offices",
            data=json.dumps(empty_governer_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422 (Unprocessable Entity)"
        )
        self.assertEqual(
            deserialized_response["error"], "Unprocessable Entity - Invalid value in data field",
            msg="Response Body Contents- Should be custom message "
        )

        response = self.client().post(
            "/api/v1/offices",
            data=json.dumps(empty_local_govt_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422 (Unprocessable Entity) "
        )
        self.assertEqual(
            deserialized_response["error"], "Unprocessable Entity - Invalid value in data field",
            msg="Response Body Contents- Should be custom message "
        )

    # def test_office_creation_with_invalid_value_types(self):
        # """ Test with invalid value types  - 422 (Unprocessable Entity) """
        # invalid_types_legislative_name_data = {
            # "name": 1,
            # "type": "Legislative"
        # }

        # invalid_types_legislative_type_data = {
            # "name": "Memnber of Congress",
            # "type": ["Legislative"]
        # }

        # response = self.client().post(
            # "/api/v1/offices",
            # data=json.dumps(invalid_types_legislative_name_data),
            # headers={'content-type': 'application/json'}
        # )
        # deserialized_response = json.loads(response.data.decode())
        # self.assertEqual(
            # response.status_code, 422,
            # msg="response code SHOULD BE 422 (Unprocessable Entity)"
        # )
        # self.assertEqual(
            # deserialized_response["error"],
            # "Unprocessable Entity - Invalid value in data field",
            # msg="Response Body Contents- Should be custom message "
        # )

        # response = self.client().post(
            # "/api/v1/offices",
            # data=json.dumps(invalid_types_legislative_type_data),
            # headers={'content-type': 'application/json'}
        # )
        # deserialized_response = json.loads(response.data.decode())
        # self.assertEqual(
            # response.status_code, 422,
            # msg="response code SHOULD BE 422 (Unprocessable Entity)"
        # )
        # self.assertEqual(
            # deserialized_response["error"],
            # "Unprocessable Entity - Invalid value in data field",
            # msg="Response Body Contents- Should be custom message "
        # )

    def test_office_creation_with_already_existing_posting(self):
        """ Test that a office posting cannot be created twice """
        response = self.client().post(
            "/api/v1/offices",
            data=json.dumps(self.legislative_office_reg_data),
            headers={'content-type': 'application/json'}
        )

        response = self.client().post(
            "/api/v1/offices",
            data=json.dumps(self.legislative_office_reg_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 409,
            msg="response code SHOULD BE 409 (Conflict)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Conflict - Office already exists",
            msg="Response Body Contents- Should be custom message "
        )


if __name__ == "__main__":
    unittest.main()
