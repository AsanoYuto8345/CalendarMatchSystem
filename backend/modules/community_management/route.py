# modules/community_management/route.py

"""
C9 コミュニティ情報管理部のルーティング
エンドポイント経由で管理機能を提供する。
"""

from flask import Blueprint, request, jsonify
from .community_management import CommunityManagement

# Blueprint の定義（URLプレフィックス付き）
management_bp = Blueprint("community_management", __name__, url_prefix="/community/manage")
service = CommunityManagement()

@management_bp.route("/info", methods=["GET"])
def get_info():
    """
    M4: コミュニティ情報取得処理（管理部側）
    """
    return service.getcommunityInfo()

@management_bp.route("/update", methods=["PUT"])
def update():
    """
    M5: コミュニティ情報更新処理（管理部側）
    """
    return service.updatecommunityInfo()
