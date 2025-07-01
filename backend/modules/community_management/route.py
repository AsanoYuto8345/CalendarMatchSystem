#backend/modules/community_management/route.py
"""
C9 コミュニティ情報管理部のルーティング
エンドポイント経由で管理機能を提供する。
"""

from flask import Blueprint, request, jsonify
from .community_management import CommunityManagement

# Blueprint の定義（URLプレフィックス付き）
management_bp = Blueprint("community_management", __name__, url_prefix="/community/manage")

# サービスクラスのインスタンス化
service = CommunityManagement()

@management_bp.route("/info", methods=["GET"])
def get_info():
    """
    M4: コミュニティ情報取得処理

    Returns:
        Response: コミュニティ情報（200, 400, 404）
    """
    return service.getcommunityInfo()

@management_bp.route("/update", methods=["PUT"])
def update():
    """
    M5: コミュニティ情報更新処理

    Returns:
        Response: 成功時200, 入力エラー400
    """
    return service.updatecommunityInfo()
