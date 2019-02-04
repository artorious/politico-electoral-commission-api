#!/usr/bin/env python3
""" Configuration settings """
import os

class BaseConfig:
    """ Parent configurattions """
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    """ Development mode configurations """
    DEBUG = True

app_config = {"development": DevelopmentConfig}
