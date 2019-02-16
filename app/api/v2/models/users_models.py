# #!/usr/bin/env python3
# """ Users methods """
# from app.api.v2.models.validation_helper import ValidationHelper

# class Users(ValidationHelper):
    # def __init__(self, user_reg_data):
        # self.user_reg_data = user_reg_data

    # def validate_user_reg_data(self):
        # """ Validate Party Registartion Data"""
        # # check for expected keys
        # # check for value types
        # # check for empty fields
        # # check for empty str fields
        # # check email length
        # # check password length
        # # Check email syntax
        # # check whether email exists
        # # check whether data already exists (email and tel nad passport)
        # # check name is str and more than 1 char

        # custom_response = None
        # cartegory = "user registration"
        # if self.check_for_expected_keys_in_user_input(
                # self.party_reg_data,
                # ["first_name", "last_name", "ngondez", "email","phone_number",
                # "passport_url", "password", "confirm_password"]
        # ) is False:
            # custom_response = jsonify(self.unprocessable_data_response), 422
        # elif self.check_for_expected_value_types_in_user_input(
                # self.party_reg_data) is False:
            # custom_response = jsonify(self.unprocessable_data_response), 422
        # elif self.check_for_empty_strings_in_user_input(
                # self.party_reg_data, "party registration") is False:
            # custom_response = jsonify(self.empty_data_field_response), 422
        # elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                # "parties", "name", self.party_reg_data["name"]) is True:
            # custom_response = jsonify(self.party_already_exists_response), 409
        # elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                # "parties", "hq_address", self.party_reg_data["hq_address"]
        # ) is True:
            # custom_response = jsonify(self.hq_already_exists_response), 409
        # elif self.lookup_whether_entity_exists_in_a_table_by_attrib(
                # "parties", "logo_url", self.party_reg_data["logo_url"]) is True:
            # custom_response = jsonify(self.logo_already_exists_response), 409
        # return custom_response
        # pass

    # def create_user_account(self):
        # pass


    # def generate_token(self, user_id):
        # """ Generates the access token"""
        # pass

    # @staticmethod
    # def decode_token(token):
        # """Decodes the access token from the Authorization header."""
        # pass
