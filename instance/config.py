#!/usr/bin/env python3
""" Configuration settings """
import os

class BaseConfig:
    """ Parent configurattions """
    DEBUG = False
    SECRET = os.getenv("SECRET")
    DATABASE_URI = os.getenv("DATABASE_URL")

class DevelopmentConfig(BaseConfig):
    """ Development mode configurations """
    DEBUG = True
    JSON_SORT_KEYS = False

class TestingConfig(BaseConfig):
    """ Testing mode configurations """
    DEBUG = True
    TESTING = True
    DATABASE_URI = os.getenv("TEST_DATABASE_URL")

app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig
    }
