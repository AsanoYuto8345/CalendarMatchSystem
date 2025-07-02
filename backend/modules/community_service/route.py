# backend/modules/community_service/route.py
"""
C4 コミュニティ処理部のルーティング
各URLエンドポイントに対して、CommunityService クラスの対応メソッドを呼び出す。
担当者: 遠藤信輝
"""

from flask import Blueprint, request
from .community_service import CommunityService

# Blueprintオブジェクトの生成（プレフィックス付き）
community_bp = Blueprint("community_service", __name__, url_prefix="/api/community")

# サービスクラスのインスタンス化
service = CommunityService()

@community_bp.route("/create", methods=["POST"])
def create():
    """
    M2: コミュニティ作成処理
    """
    return service.create()

@community_bp.route("/join", methods=["POST"])
def join():
    """
    M3: コミュニティ参加処理
    """
    return service.join()

@community_bp.route("/leave", methods=["DELETE"])
def leave():
    """
    M4: コミュニティ脱退処理
    """
    return service.leave()

@community_bp.route("/template_tags", methods=["POST", "PUT", "DELETE"])
def edit_tags():
    """
    M5: テンプレートタグ編集処理
    """
    return service.edit_tags()

@community_bp.route("/template_tags", methods=["GET"])
def get_tags():
    """
    M6: テンプレートタグ取得処理
    """
    return service.get_tags()

@community_bp.route("/<string:community_id>/tag/<string:tag_id>/chat/post", methods=["POST"])
def post_chat(community_id, tag_id):
    """
    M8: チャット投稿処理
    """
    return service.post_chat(community_id, tag_id)

@community_bp.route("/<string:community_id>/tag/<string:tag_id>/chat/history", methods=["GET"])
def get_chat_history(community_id, tag_id):
    """
    M9: チャット履歴取得処理
    """
    date = request.args.get("date", "").strip()
    return service.get_chat_history(community_id, tag_id, date)

@community_bp.route("/joined", methods=["GET"])
def get_joined_communities():
    """
    M25: 所属コミュニティ一覧取得処理
    """
    return service.get_joined_communities()

@community_bp.route("/members", methods=["GET"])
def get_community_members():
    """
    M7: コミュニティ所属メンバー取得処理
    """
    return service.get_community_members()

@community_bp.route("/info_by_id", methods=["GET"])
def get_community_info_by_id():
    """
    M10: コミュニティIDから情報取得
    """
    return service.get_community_info_by_id()

@community_bp.route("/info_by_tag", methods=["GET"])
def get_community_info_by_tag_id():
    """
    M11: テンプレートタグIDからコミュニティ情報取得
    """
    return service.get_community_info_by_tag_id()

@community_bp.route("/members_by_tag", methods=["GET"])
def get_community_members_by_tag():
    """
    M12: テンプレートタグIDからコミュニティメンバー取得
    """
    return service.get_community_members_by_tag_id()
