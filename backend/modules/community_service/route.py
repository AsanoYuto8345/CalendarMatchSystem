"""
C4 コミュニティ処理部ルーティング
作成者: 遠藤信輝
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import logging

from .community_service import (
    create_community,
    join_community,
    leave_community,
    handle_template_tags
)

community_bp = Blueprint("community", __name__)
logger = logging.getLogger(__name__)

@community_bp.before_request
def log_request():
    logger.debug(f"{request.method} {request.path}")
    logger.debug(f"Content-Type: {request.content_type}, Length: {request.content_length}")

@community_bp.route("/community/create", methods=["OPTIONS", "GET", "POST"])
@cross_origin()
def route_create_community():
    if request.method == 'OPTIONS':
        return '', 200
    if request.method == 'GET':
        return jsonify({"message": "GET request received"}), 200
    return create_community()

@community_bp.route("/community/join", methods=["POST"])
@cross_origin()
def route_join_community():
    return join_community()

@community_bp.route("/community/leave", methods=["POST"])
@cross_origin()
def route_leave_community():
    return leave_community()

@community_bp.route("/community/template_tags", methods=["GET", "POST", "PUT", "DELETE"])
@cross_origin()
def route_template_tags():
    return handle_template_tags()
