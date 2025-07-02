# backend/modules/community_management/route.py
"""
C9 コミュニティ情報管理部のルーティング
エンドポイント経由で管理機能を提供する。
"""

from flask import Blueprint, request
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


@management_bp.route("/<community_id>/tag/<tag_id>/chat", methods=["POST"])
def post_chat(community_id, tag_id):
    """
    M8: チャット送信処理

    Returns:
        Response: 送信成功201, 入力不正400, 保存失敗500
    """
    return service.post_chat(community_id, tag_id, request.get_json())


@management_bp.route("/<community_id>/tag/<tag_id>/chat", methods=["GET"])
def get_chat(community_id, tag_id):
    """
    M9: チャット履歴取得処理

    クエリ:
        ?date=YYYY-MM-DD

    Returns:
        Response: 履歴取得成功200, エラー400/500
    """
    date = request.args.get("date", "").strip()
    return service.get_chat_history(community_id, tag_id, date)

@management_bp.route("/user/<user_id>/communities-tags", methods=["GET"])
def get_communities_tags_by_user(user_id):
    """
    M1: ユーザIDからコミュニティ＋テンプレートタグ取得

    Returns:
        Response: 200 OK or 400 Bad Request
    """
    return service.get_communities_and_tags_by_user(user_id)
