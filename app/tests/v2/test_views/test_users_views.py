#!/usr/bin/env python3
""" Test Cases for Users Views/Routes """
import unittest
import json
from app import create_app
from app.api.v2.models.database_models import DatabaseManager


class TestUserRoutes(unittest.TestCase):
    """ Parent test case for all Users related views """

    def setUp(self):
        """ Initialize app and test variables """
        self.app = create_app(config_mode="testing")
        with self.app.app_context():
            self.client = self.app.test_client

            self.user_reg_data = {
                "first_name": "arthur",
                "last_name": "ngondo",
                "other_name": "ngondez",
                "email": "ngondez@email.com",
                "telephone": "+254727161173",
                "passport_url": "images/arthur.jpg",
                "password": "apassword",
                "confirm_password": "apassword"
            }

    def tearDown(self):
        with self.app.app_context():
            db = DatabaseManager()
            db.drop_tables()


class TestUserCreation(TestUserRoutes):
    """ Test Cases for user signup"""

    def test_user_signup_with_valid_data(self):
        """ Test user account creation with valid data """
        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(self.user_reg_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertIn("user", deserialized_response)
        self.assertIn("authentication token", deserialized_response["user"][0])
        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (created)"
        )

    def test_user_signup_with_empty_strings(self):
        """ Test with an empty string in field - unprocessable"""
        sample_user = {
                "first_name": "",
                "last_name": "ngondo",
                "other_name": "ngondez",
                "email": "ngondez@email.com",
                "telephone": "+254727161173",
                "passport_url": "iamges/arthur.jpg",
                "password": "apassword",
                "confirm_password": "apassword"
            }
        sample_user1 = {
                "first_name": "arthur",
                "last_name": "\t",
                "other_name": "ngondez",
                "email": "ngondez@email.com",
                "telephone": "+254727161173",
                "passport_url": "iamges/arthur.jpg",
                "password": "apassword",
                "confirm_password": "apassword"
            }
        sample_user2 = {
                "first_name": "arthur",
                "last_name": "ngondo",
                "other_name": "\n",
                "email": "ngondez@email.com",
                "telephone": "+254727161173",
                "passport_url": "iamges/arthur.jpg",
                "password": "apassword",
                "confirm_password": "apassword"
            }
        sample_user3 = {
                "first_name": "arthur",
                "last_name": "ngondo",
                "other_name": "ngondez",
                "email": "             ",
                "telephone": "+254727161173",
                "passport_url": "iamges/arthur.jpg",
                "password": "apassword",
                "confirm_password": "apassword"
            }

        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(sample_user),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422 (Unprocessable Entity)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Empty data field",
            msg="Response Body Contents- Should be custom message "
        )

        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(sample_user1),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422 (Unprocessable Entity)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Empty data field",
            msg="Response Body Contents- Should be custom message "
        )

        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(sample_user2),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422 (Unprocessable Entity)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Empty data field",
            msg="Response Body Contents- Should be custom message "
        )

        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(sample_user3),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422 (Unprocessable Entity)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Empty data field",
            msg="Response Body Contents- Should be custom message "
        )

    def test_user_signup_with_less_fields(self):
        """ Test with less fields than expected. """
        test_less_data = {
            "first_name": "arthur",
            "last_name": "ngondo",
            "other_name": "ngondez",
            "email": "ngondez@email.com",
            "telephone": "+254727161173",
            "passport_url": "iamges/arthur.jpg",
            "password": "apassword"
        }
        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(test_less_data),
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

    def test_user_signup_with_more_fileds(self):
        """ Test with more fields than expected. """
        test_extra_data = {
            "first_name": "arthur",
            "last_name": "ngondo",
            "other_name": "ngondez",
            "email": "ngondez@email.com",
            "telephone": "+254727161173",
            "passport_url": "iamges/arthur.jpg",
            "password": "apassword",
            "confirm_password": "apassword",
            "sneak": "I'm not supposed to be here"
        }

        response = self.client().post(
            "/api/v2/auth/signup",
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

    def test_user_signup_with_invalid_email_syntax(self):
        """ Test user creation with invalid email syntax """
        sample_user = {
                "first_name": "Bruce",
                "last_name": "Willis",
                "other_name": "logic",
                "email": "ngondez#email.com",
                "telephone": "+254345678",
                "passport_url": "iamges/logic.jpg",
                "password": "apassword",
                "confirm_password": "apassword"
            }
        sample_user1 = {
                "first_name": "Tavis",
                "last_name": "Scott",
                "other_name": "kidcudi",
                "email": "ngondez@emailcom",
                "telephone": "+25472755555",
                "passport_url": "iamges/kidcudi.jpg",
                "password": "apassword",
                "confirm_password": "apassword"
            }

        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(sample_user),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422")

        self.assertIn("error", deserialized_response)
        self.assertEqual(
            deserialized_response["error"],
            "Invalid Email Syntax",
            msg="Response Body Contents- Should be custom message "
        )

        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(sample_user1),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422")
        self.assertIn("error", deserialized_response)
        self.assertEqual(
            deserialized_response["error"],
            "Invalid Email Syntax",
            msg="Response Body Contents- Should be custom message "
        )

    def test_user_signup_with_invalid_password_length(self):
        """ Test user account creation with invalid password length """
        sample_user = {
                "first_name": "Joe",
                "last_name": "Cole",
                "other_name": "jcole",
                "email": "cole@email.com",
                "telephone": "+254727161278",
                "passport_url": "images/cole.jpg",
                "password": "passwd",
                "confirm_password": "passwd"
            }
        sample_user1 = {
                "first_name": "Joey",
                "last_name": "Badass",
                "other_name": "Bada$$",
                "email": "joey@email.com",
                "telephone": "+254727162273",
                "passport_url": "images/arthur.jpg",
                "password": "\t\tpass\t",
                "confirm_password": "\t\tpass\t"
            }
        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(sample_user1),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422")
        self.assertIn("error", deserialized_response)
        self.assertEqual(
            deserialized_response["error"],
            "Invalid Password Length. 6 Characters minimum",
            msg="Response Body Contents- Should be custom message "
        )

        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(sample_user),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422")
        self.assertIn("error", deserialized_response)
        self.assertEqual(
            deserialized_response["error"],
            "Invalid Password Length. 6 Characters minimum",
            msg="Response Body Contents- Should be custom message "
        )

    def test_user_signup_with_mismatched_passwords(self):
        """ Test office creation with mismatched passwords """
        sample_user = {
                "first_name": "arthur",
                "last_name": "ngondo",
                "other_name": "ngondez",
                "email": "ngondez@email.com",
                "telephone": "+254727161173",
                "passport_url": "iamges/arthur.jpg",
                "password": "apassword1",
                "confirm_password": "apassword2"
            }

        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(sample_user),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertEqual(
            response.status_code, 422,
            msg="response code SHOULD BE 422")
        self.assertIn("error", deserialized_response)
        self.assertEqual(
            deserialized_response["error"],
            "Passwords do not match",
            msg="Response Body Contents- Should be custom message "
        )

    def test_user_signup_with_an_already_registered_email(self):
        """  Test with email that is already in use """
        sample_data = {
                "first_name": "A-boul",
                "last_name": "Kamau",
                "other_name": "solo",
                "email": "ngondez@email.com",
                "telephone": "+254123456789",
                "passport_url": "images/absoul.jpg",
                "password": "apassword",
                "confirm_password": "apassword"
            }
        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(self.user_reg_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertIn("user", deserialized_response)
        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (created)"
        )

        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(sample_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertIn("error", deserialized_response)
        self.assertEqual(
            response.status_code, 409,
            msg="response code SHOULD BE 409"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Conflict - Email already in use",
            msg="Response Body Contents- Should be custom message "
        )

    def test_user_signup_with_an_already_registered_passport_url(self):
        """  Test with passport_url that is already in use """
        sample_user = {
                "first_name": "arthur",
                "last_name": "ngondo",
                "other_name": "ngondez",
                "email": "unique@email.com",
                "telephone": "+254123456789",
                "passport_url": "images/arthur.jpg",
                "password": "apassword1",
                "confirm_password": "apassword1"
            }
        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(self.user_reg_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertIn("user", deserialized_response)
        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (created)"
        )

        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(sample_user),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertIn("error", deserialized_response)
        self.assertEqual(
            response.status_code, 409,
            msg="response code SHOULD BE 409)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Conflict - Passport photo already in use",
            msg="Response Body Contents- Should be custom message "
        )

    def test_user_signup_with_an_already_registered_cell_no(self):
        """  Test with telephone number that is already in use """
        sample_user = {
                "first_name": "David",
                "last_name": "Waithaka",
                "other_name": "Ngondo",
                "email": "unique@email.com",
                "telephone": "+254727161173",
                "passport_url": "images/newimage.jpg",
                "password": "apassword1",
                "confirm_password": "apassword1"
            }
        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(self.user_reg_data),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertIn("user", deserialized_response)
        self.assertEqual(
            response.status_code, 201,
            msg="response code SHOULD BE 201 (created)"
        )

        response = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(sample_user),
            headers={'content-type': 'application/json'}
        )
        deserialized_response = json.loads(response.data.decode())
        self.assertIn("error", deserialized_response)
        self.assertEqual(
            response.status_code, 409,
            msg="response code SHOULD BE 409)"
        )
        self.assertEqual(
            deserialized_response["error"],
            "Conflict - Phone number already registered",
            msg="Response Body Contents- Should be custom message "
        )


if __name__ == "__main__":
    unittest.main()
