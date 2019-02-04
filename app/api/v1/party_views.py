#!/usr/bin/env python3
""" Political party views """

from flask import Blueprint, jsonify, request
from app.api.v1.party_models import PoliticalParties

base_bp_v1 = Blueprint("v1_base", __name__, url_prefix="/api/v1")


@base_bp_v1.route("/parties", methods=["POST"])
def parties():
    if request.method == "POST":
        # Request user data
        # 
        pass
    else:
        pass



