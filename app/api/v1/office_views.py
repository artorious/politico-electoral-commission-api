#!/usr/bin/env python3
""" Routes Office Information """

from flask import Blueprint, jsonify, request

OFFICE_BP_V1 = Blueprint("v1_office", __name__, url_prefix="/api/v1")

@OFFICE_BP_V1.route("/offices", methods=["GET"])
def offices():
    return jsonify("YaH")



