#!/usr/bin/env python3
""" Holds methods for handling Users data """
from flask import current_app, jsonify
import jwt
import time
import psycopg2
import bcrypt
from datetime import datetime, timedelta
from app.api.v2.models.validation_helper import ValidationHelper


class Users(ValidationHelper):
    """ Holds methods for users """
    def __init__(self, user_reg_data):
        self.user_reg_data = user_reg_data
        self.raw_password = user_reg_data["password"]
        super().__init__()

    def validate_user_reg_data(self):
        """ Validate Party Registartion Data"""

        custom_response = None

        if self.check_for_expected_keys_in_user_input(self.user_reg_data, [
                "first_name", "last_name", "other_name", "email", "telephone",
                "passport_url", "password", "confirm_password"]
        ) is False:
            custom_response = jsonify(self.unprocessable_data_response), 422

        elif self.check_for_expected_value_types_in_user_input(
                self.user_reg_data) is False:
            custom_response = jsonify(self.unexpected_data_types_resp), 422

        elif len(self.raw_password.strip()) < 7:
            custom_response = jsonify(self.invalid_password_length_resp), 422

        elif self.user_reg_data["password"] != \
                self.user_reg_data["confirm_password"]:
            custom_response = jsonify(self.mismatched_email_resp), 422

        elif self.check_for_empty_strings_in_user_input(
                self.user_reg_data) is True:
            custom_response = jsonify(self.empty_data_field_response), 422

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "users", "email", self.user_reg_data["email"]) is True:
            custom_response = jsonify(self.email_already_exists_response), 409

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "users", "passport_url", self.user_reg_data["passport_url"]
        ) is True:
            custom_response = jsonify(
                self.passport_already_exists_response), 409

        elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                "users", "telephone", self.user_reg_data["telephone"]
        ) is True:
            custom_response = jsonify(
                self.telephone_already_exists_response), 409

        elif self.check_valid_email_syntax(self.user_reg_data["email"]) is None:
            custom_response = jsonify(self.invalid_email_syntax_resp), 422

        return custom_response

    def create_user_account(self):
        """ Create user Account"""
        time_obj = time.localtime(time.time())
        password = self.user_reg_data["password"]
        encoded_password = password.encode()
        hashed_password = bcrypt.hashpw(
            encoded_password, bcrypt.gensalt()).decode()

        custom_msg = None
        try:
            self.cursor.execute("""
            INSERT INTO users (uid, firstname, lastname, othername,
            email, telephone, passport_url,registration_timestamp,
            last_login_timestamp, is_admin, password)
            VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING uid;""", (
                self.user_reg_data["first_name"],
                self.user_reg_data["last_name"],
                self.user_reg_data["other_name"],
                self.user_reg_data["email"],
                self.user_reg_data["telephone"],
                self.user_reg_data["passport_url"],
                time.asctime(time_obj),
                "Not logged in Yet",
                False,
                hashed_password
            ))

            last_id = self.cursor.fetchall()
            uid = last_id[0]["uid"]
            auth_token_byte_str = self.generate_token(uid)
            custom_msg = {"status": 201, "user": [{
                "authentication token": auth_token_byte_str,
                "login email": self.user_reg_data["email"],
                "Message": "Registration successful please login"
            }]}

        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

        finally:
            return custom_msg

    @staticmethod
    def generate_token(uid):
        """ Generates and returns the access token byte string """
        print(f"#########-> {uid} -- {type(uid)}")
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow(),
                'sub': uid
            }
            token_byte_str = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            ).decode('utf-8')
            return token_byte_str
        except Exception as err:
            return str(err)


    def __repr__(self):
        """ Return current user name """
        return f'User Login Email - {self.user_reg_data["email"]}'



