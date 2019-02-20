#!/usr/bin/env python3
""" Test Cases for candidate Views/Routes """
import unittest
import json
from app import create_app
from app.api.v2.models.database_models import DatabaseManager

class TestCandidatesRoutes(unittest.TestCase):
    """ Parent test case for all Candidate related views
        tests for candidate registration and expression of interest
    """

    def setUp(self):
        """ Initialize app and test variables """
        self.app = create_app(config_mode="testing")
        with self.app.app_context():
            self.client = self.app.test_client
            #Admin Login
            self.test_admin_login_data = {
                "email": "shirleen@admin.com", "password": "iambaboon"}
            login_results = self.client().post(
                "/api/v2/auth/login", data=json.dumps(
                    self.test_admin_login_data))
            auth_token = json.loads(login_results.data)["message"][0]["token"]
            self.updated_header = {
                "content-type": "application/json",
                "Authorization": f"Bearer {auth_token}"}
            # Sample User
            self.test_user_signup_data = {
                "first_name": "Florence",
                "last_name": "Ruguru",
                "other_name": "flojo",
                "email": "ruguru@email.com",
                "telephone": "+25418980",
                "passport_url": "images/flo.jpg",
                "password": "abcdefghijkl",
                "confirm_password": "abcdefghijkl"
            }
            self.test_user_login_data = {
                "email": "ruguru@email.com", "password": "abcdefghijkl"}
            resp = self.client().post("/api/v2/auth/signup", data=json.dumps(self.test_user_signup_data))
            login_results = self.client().post("/api/v2/auth/login", data=json.dumps(self.test_user_login_data))
            auth_token = json.loads(login_results.data)["message"][0]["token"]
            self.updated_header = {"content-type": "application/json", "Authorization": f"Bearer {auth_token}"}

            # Sample Office
            self.state_office_reg_data = {
                "name": "Governor",
                "type": "State",
            }
            response = self.client().post(
            "/api/v2/offices",
            data=json.dumps(
                self.state_office_reg_data),
                headers=self.updated_header)

            # Sample Party
            self.party_reg_data = {
                "name": "Jubilee",
                "hq_address": "Jubilee Tower, Pangani, Thika Road",
                "logo_url": "/static/jubilee.jpeg"
            }
            resp = self.client().post(
                "/api/v2/parties",
                data=json.dumps(self.party_reg_data),
                headers=self.updated_header)

            self.sample_candidate_payload = {"user_id": 2, "party_id": 1, "office_id": 1}

    def tearDown(self):
        with self.app.app_context():
            db = DatabaseManager()
            db.drop_tables()

class TestCandidateCreation(TestCandidatesRoutes):
    """ Tests for creating a candidate for office """

    def test_candidate_registration_with_valid_details(self):
        """ Test that a valid candidate is registered """
        response = self.client().post(
            "/api/v2/office/1/register",
            data=json.dumps(self.sample_candidate_payload),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertIn("candidate", deserialized_response)

        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (created)"
        )

    def test_with_an_already_registered_candidate(self):
        """ Ensure candidate is not registered twice or the same office """
        response = self.client().post(
            "/api/v2/office/1/register",
            data=json.dumps(self.sample_candidate_payload),
            headers=self.updated_header
        )
        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (created)"
        )
        response = self.client().post(
            "/api/v2/office/1/register",
            data=json.dumps(self.sample_candidate_payload),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertIn("error", deserialized_response)
        self.assertEqual(
            response.status_code, 409,
            msg="response code SHOULD BE 409"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Conflict - Candidate  already registerd for this office",
            msg="Response Body Contents- Should be custom message "
        )


    def test_with_zero_or_negative_as_ids(self):
        """ Handling of zero or negative ids in payload"""

        response = self.client().post(
            "/api/v2/office/1/register",
            data=json.dumps({"uid": 2, "pid": 0}),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="Should be 400 status"
        )
        self.assertEqual(
            deserialized_response["error"],
            'ID cannot be zero or negative',
            msg="Response Body Contents- Should be custom message "
        )

        response = self.client().post(
            "/api/v2/office/1/register",
            data=json.dumps({"uid": 0, "pid": 1}),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="Should be 400 status"
        )
        self.assertEqual(
            deserialized_response["error"],
            'ID cannot be zero or negative',
            msg="Response Body Contents- Should be custom message "
        )

        response = self.client().post(
            "/api/v2/office/1/register",
            data=json.dumps({"uid": 2, "pid": -1}),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="Should be 400 status"
        )
        self.assertEqual(
            deserialized_response["error"],
            'ID cannot be zero or negative',
            msg="Response Body Contents- Should be custom message "
        )

    def test_with_a_positive_out_int_as_office_id(self):
        """ Handle out of range or Ids that dont exist"""
        response = self.client().post(
            "/api/v2/office/0/register",
            data=json.dumps(self.sample_candidate_payload),
            headers=self.updated_header
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

        response = self.client().post(
            "/api/v2/office/-1/register",
            data=json.dumps(self.sample_candidate_payload),
            headers=self.updated_header
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


    def test_with_a_party_id_that_doesnt_exist(self):
        """ Handle registration with party Ids that dont exist"""
        pass

    def test_with_a_office_id_that_doesnt_exist(self):
        """ Handle registration with office Ids that dont exist"""
        pass

    def test_with_a_user_id_that_doesnt_exist(self):
        """ Handle registration with user Ids that dont exist"""
        pass

    def test_with_non_integers_in_the_payload(self):
        """ Handle non-ntegers in payload"""
        response = self.client().post(
            "/api/v2/office/1/register",
            data=json.dumps({"uid": 2.2, "pid": 0}),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="Should be 400 status"
        )
        self.assertEqual(
            deserialized_response["error"],
            'ID cannot be zero or negative',
            msg="Response Body Contents- Should be custom message "
        )

        response = self.client().post(
            "/api/v2/office/1/register",
            data=json.dumps({"uid": "one" , "pid": 1}),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="Should be 400 status"
        )
        self.assertEqual(
            deserialized_response["error"],
            'ID cannot be zero or negative',
            msg="Response Body Contents- Should be custom message "
        )



    def test_with_more_fields_in_the_payload_than_expected(self):
        """ Test with more fields than expected. """
        response = self.client().post(
            "/api/v2/office/1/register",
            data=json.dumps({"uid": 1, "pid": 1, "kid": 5}),
            headers=self.updated_header
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


    def test_with_less_fields_than_expected(self):
        """ Test with fewer fields than expected. """
        response = self.client().post(
            "/api/v2/office/1/register",
            data=json.dumps({"uid": 1}),
            headers=self.updated_header
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 400,
            msg="response code SHOULD BE 400 (bad query)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Bad Query - Less data fields than expected.",
            msg="Response Body Contents- Should be custom message "
        )

    def test_with_a_wrong_request_method(self):
        pass

    def test_attempted_access_by_user_who_is_not_admin(self):
        pass


if __name__ == "__main__":
    unittest.main()
