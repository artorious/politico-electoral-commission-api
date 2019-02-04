#!/usr/bin/env python3
""" Configuration settings """
import os

class BaseConfig:
    """ Parent configurattions """
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    """ Development mode configurations """
    DEBUG = True

class TestingConfig(BaseConfig):
    """ Testing mode configurations """
    DEBUG = True
    TESTING = True

app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig
    }
