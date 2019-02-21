#!/usr/bin/env python3
""" Methods for querying the database """
import os
import sys
import time
import psycopg2
import bcrypt
import psycopg2.extras
from flask import current_app


class DatabaseManager:
    """ Database Manager """
    parties_table_query = "CREATE TABLE IF NOT EXISTS parties (\
            pid SERIAL PRIMARY KEY, \
            name VARCHAR(50) UNIQUE NOT NULL,\
            hq_address VARCHAR(50) UNIQUE NOT NULL, \
            logo_url TEXT UNIQUE NOT NULL, \
            registration_timestamp VARCHAR(50) NOT NULL \
            );"

    offices_table_query = "CREATE TABLE IF NOT EXISTS offices (\
            oid SERIAL PRIMARY KEY, \
            name VARCHAR(50) UNIQUE NOT NULL,\
            type VARCHAR(50) NOT NULL CHECK (type IN \
            ('Federal', 'Legislative', 'State', 'Local Government')), \
            registration_timestamp VARCHAR(50) NOT NULL \
            );"

    users_table_query = "CREATE TABLE IF NOT EXISTS users (\
            uid SERIAL PRIMARY KEY, \
            firstname VARCHAR(50) NOT NULL, \
            lastname VARCHAR(50) NOT NULL, \
            othername VARCHAR(50) NOT NULL, \
            email VARCHAR(50) UNIQUE NOT NULL, \
            telephone VARCHAR(50) UNIQUE NOT NULL, \
            passport_url TEXT UNIQUE NOT NULL, \
            registration_timestamp VARCHAR(50) NOT NULL, \
            last_login_timestamp VARCHAR(50) NOT NULL, \
            is_admin BOOLEAN NOT NULL, \
            password VARCHAR NOT NULL \
            );"

    candidate_table_query = "CREATE TABLE IF NOT EXISTS candidates (\
            cid SERIAL, \
            oid INT NOT NULL,\
            uid INT NOT NULL,\
            pid INT NOT NULL, \
            registration_timestamp VARCHAR(50) NOT NULL, \
            PRIMARY KEY (oid, uid) \
            );"
    votes_table_query = "CREATE TABLE IF NOT EXISTS votes (\
            vid SERIAL, \
            cid INT NOT NULL,\
            uid INT NOT NULL, \
            oid INT NOT NULL,\
            pid INT NOT NULL,\
            registration_timestamp VARCHAR(50) NOT NULL, \
            PRIMARY KEY (oid, uid) \
            );"
    petitions_table_query = "CREATE TABLE IF NOT EXISTS petitions (\
            petition_id SERIAL PRIMARY KEY, \
            office INT NOT NULL,\
            cover_letter TEXT NOT NULL, \
            evidence TEXT, \
            registration_timestamp VARCHAR(50) NOT NULL\
            );"

    time_obj = time.localtime(time.time())
    default_admin = """
            INSERT INTO users (uid, firstname, lastname, othername,
            email, telephone, passport_url,registration_timestamp,
            last_login_timestamp, is_admin, password)
            VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (
                "Shirleen", "Njoki", "koki", os.getenv("ADMIN_EMAIL"),
                "0727212166", "images/koki.png", time.asctime(time_obj),
                "Not logged in Yet", True, os.getenv("DEFAULT_ADMIN_PASS"))

    def __init__(self):
        """ Initaliaze a cursor connection to DB """
        self.conn = None
        try:
            self.conn = psycopg2.connect(current_app.config['DATABASE_URI'])
            self.conn.autocommit = True
            self.cursor = self.conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            )

        except psycopg2.DatabaseError as err:
            print(f"Error connecting to DB: {err}")

    def create_all_tables(self):
        """ Create all Tables """
        self.cursor.execute(self.parties_table_query)
        self.cursor.execute(self.offices_table_query)
        self.cursor.execute(self.users_table_query)
        self.cursor.execute(self.candidate_table_query)
        self.cursor.execute(self.votes_table_query)
        self.cursor.execute(self.petitions_table_query)
        print("Tables Created Succesfully")

    def fetch_all_records_in_a_table(self, table):
        """ Fetches all records from <table> in the database """
        custom_msg = None
        try:
            self.cursor.execute(f"select * from {table};")
            custom_msg = self.cursor.fetchall()
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)
        finally:
            return custom_msg

    def fetch_a_record_by_id_from_a_table(self, table, entity_id, id_value):
        """ Fetch a single record from DB """
        custom_msg = None
        try:
            self.cursor.execute(
                f"select * from {table} where {entity_id}={id_value};"
                )
            custom_msg = self.cursor.fetchall()
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)
        finally:
            return custom_msg

    def lookup_whether_entity_exists_in_a_table_by_attrib(
            self, table, attrib, value
    ):
        """ Checks for <value> in <table> on colunm <atrrib>  in DB,
            returns True if it exists, else False
        """
        try:
            self.cursor.execute(
                f"SELECT * from {table} WHERE {attrib}='{value}';"
            )
            entity_fetch = self.cursor.fetchone()
            if entity_fetch is None:
                msg_out = False
            else:
                msg_out = True
            return msg_out
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

    def edit_a_table_record(self, table, entity_id, new_data):
        """ Edit/update a record """
        custom_msg = None
        try:
            self.cursor.execute(
                f"update {table} set name = '{new_data['name']}' " +
                f"where pid={entity_id} returning pid, name;"
            )
            response = self.cursor.fetchall()
            custom_msg = {
                "Party Id": response[0]["pid"],
                "New Party Name": response[0]["name"]}
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)
        finally:
            return custom_msg

    def delete_a_table_record(self, table, entity_id):
        """ Delete a database record from <table> in Database """
        custom_msg = None
        try:
            self.cursor.execute(f"delete from {table} where pid={entity_id};")
            custom_msg = f"Party No. {entity_id} deleted succesfully"
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)
        finally:
            return custom_msg

    def drop_tables(self):
        """ Drop all tables """
        try:
            self.cursor.execute("DROP TABLE IF EXISTS parties CASCADE")
            self.cursor.execute("DROP TABLE IF EXISTS offices CASCADE")
            self.cursor.execute("DROP TABLE IF EXISTS users CASCADE")
            self.cursor.execute("DROP TABLE IF EXISTS candidates CASCADE")
            self.cursor.execute("DROP TABLE IF EXISTS votes CASCADE")
            print("Tables Dropped Successfully")
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

    def db_error_handler(self, error):
        """ Roll back transaction and exit incase of error """
        if self.conn:
            self.conn.rollback()
            print('An Error Occured: {}'.format(error))
            sys.exit(1)

    def close_database(self):
        """ Closes database connection """
        if self.conn:
            self.conn.close()

    def fetch_entity_id(self, id_type, table, attrib, value):
        """ Fetch ID from <table> where <attrib> is <value> """
        try:
            self.cursor.execute(
                f"SELECT * from {table} WHERE {attrib}='{value}';"
            )
            user_record = self.cursor.fetchall()
            fetched_id = user_record[0][id_type]

            return fetched_id
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

    def verify_user_password(self, password, email):
        """
        Checks the password against it's hash to validates the user's password
        Truthy
        """
        unverified_password = password.encode()
        try:
            self.cursor.execute(
                f"SELECT * from users WHERE email='{email}';"
            )
            user_record = self.cursor.fetchall()
            hashed_password_str = user_record[0]["password"]

            hashed_password_bytes = hashed_password_str.encode()
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

        return bcrypt.checkpw(unverified_password, hashed_password_bytes)

    def update_login_timestamp(self, email):
        time_obj = time.localtime(time.time())
        try:
            self.cursor.execute(
                f"update users set last_login_timestamp = '{time.asctime(time_obj)}' " +
                f"where email='{email}';"
            )
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

    def is_admin(self, uid):
        """ Check if uer is admin """
        self.cursor.execute(f"SELECT * from users WHERE uid={uid};")
        resp = self.cursor.fetchall()
        return resp[0]["is_admin"]
