#!/usr/bin/env python3
""" Political party views """
from flask import Blueprint, jsonify, request

PARTY_BP_V2 = Blueprint("v2_party", __name__, url_prefix="/api/v2")

@PARTY_BP_V2.route("/parties", methods=["GET"])
def fetch_all_parties():
    """ Fetch all political parties """
    pass


@PARTY_BP_V2.route("/parties", methods=["POST"])
def create_a_party():
    """ Fetch all political parties """
    pass


@PARTY_BP_V2.route("/parties/<int:pid>", methods=["GET"])
def fetch_a_party(pid):
    """(Fetch a political party  by ID """
    pass


@PARTY_BP_V2.route("/parties/<int:pid>", methods=["DELETE"])
def delete_a_party(pid):
    """DELETE a political party  by ID """
    pass


@PARTY_BP_V2.route("/parties/<int:pid>/name", methods=["PATCH"])
def party_manager(pid):
    """ Edit politcal party  name by ID"""
    pass