# C4 コミュニティ処理部のルーティング　担当: 遠藤信輝

from flask import Blueprint, request
from .community_service import CommunityService

community_bp = Blueprint("community", __name__, url_prefix="/api/community")
service = CommunityService()

@community_bp.route("/create", methods=["POST"])
def create():
    return service.create()

@community_bp.route("/join", methods=["POST"])
def join():
    return service.join()

@community_bp.route("/leave", methods=["DELETE"])
def leave():
    return service.leave()

@community_bp.route("/template_tags", methods=["POST", "PUT", "DELETE"])
def edit_tags():
    return service.edit_tags()

@community_bp.route("/template_tags", methods=["GET"])
def get_tags():
    return service.get_tags()
