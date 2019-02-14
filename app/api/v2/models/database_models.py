#!/usr/bin/env python3
""" Methods for querying the database """
import sys
import psycopg2
import psycopg2.extras
from flask import current_app

class DatabaseManager:
    """ Database Manager  """
    parties_table_query = "CREATE TABLE IF NOT EXISTS parties (\
            pid SERIAL PRIMARY KEY, \
            name VARCHAR(50) UNIQUE NOT NULL,\
            hq_address VARCHAR(50) NOT NULL, \
            logo_url VARCHAR(50) NOT NULL, \
            registration_timestamp VARCHAR(50) NOT NULL \
            );"

    offices_table_query = "CREATE TABLE IF NOT EXISTS offices (\
            oid SERIAL PRIMARY KEY, \
            name VARCHAR(50) UNIQUE NOT NULL,\
            type VARCHAR(25) NOT NULL CHECK (type IN ('Federal', 'Legislative', 'State', 'Local Government')), \
            registration_timestamp VARCHAR(50) NOT NULL \
            );"

    def __init__(self):
        """ Initaliaze a cursor connection to DB """
        self.conn = None
        try:
            self.conn = psycopg2.connect(current_app.config['DATABASE_URI'])
            self.conn.autocommit = True
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            #self.cursor = self.conn.cursor()
        except psycopg2.DatabaseError as err:
            print(f"Error connecting to DB: {err}")


    def create_a_table(self, table_query):
        pass

    def create_all_tables(self):
        """ Create all Tables """
        self.cursor.execute(self.parties_table_query)
        self.cursor.execute(self.offices_table_query)
        print("Tables Created Succesfully")

    def insert_a_validated_record_into_table(self, table, user_data):
        pass

    def fetch_all_records_in_a_table(self, table):
        custom_msg = None
        try:
            self.cursor.execute(f"select * from {table};")
            custom_msg = self.cursor.fetchall()
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)
        finally:
            return custom_msg

    def fetch_a_record_by_id_from_a_table(self, table, entity_id):
        custom_msg = None
        try:
            self.cursor.execute(f"select * from {table} where pid={entity_id};")
            custom_msg = self.cursor.fetchall()
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)
        finally:
            return custom_msg

    def lookup_whether_entity_exists_in_a_table_by_attrib(self, table, attrib, value):
        """ Checks for <value> in <table> on colunm <atrrib>  in DB, 
            returns True if it exists, else False
        """
        try:
            self.cursor.execute(f"SELECT * from {table} WHERE {attrib}='{value}';")
            entity_fetch = self.cursor.fetchone()
            if entity_fetch == None:
                msg_out = False
            else:
                msg_out = True
            return msg_out
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)


    def edit_a_table_record(self, table, entity_id, new_data):
        pass

    def delete_a_table_record(self, table, entity_id):
        pass

    def tally_an_entity(self, table, count_item):
        pass

    def drop_tables(self):
        """ Drop all tables """
        try:
            self.cursor.execute("DROP TABLE IF EXISTS parties CASCADE")
            self.cursor.execute("DROP TABLE IF EXISTS offices CASCADE")
            print("Tables Dropped Successfully")
        except psycopg2.DatabaseError as err:
            self.db_error_handler(err)

    def drop_table(self):
        pass

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