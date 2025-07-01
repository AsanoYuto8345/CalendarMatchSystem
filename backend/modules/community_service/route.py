#backend/modules/community_service/route.py
"""
C4 コミュニティ処理部のルーティング
各URLエンドポイントに対して、CommunityService クラスの対応メソッドを呼び出す。
担当者: 遠藤信輝
"""

from flask import Blueprint, request, jsonify
from .community_service import CommunityService

# Blueprintオブジェクトの生成（プレフィックス付き）
community_bp = Blueprint("community_service", __name__, url_prefix="/api/community")

# サービスクラスのインスタンス化
service = CommunityService()

# コーディング規約: 各関数に簡潔なdocstringを付与

@community_bp.route("/create", methods=["POST"])
def create():
    """
    M2: コミュニティ作成処理

    Returns:
        Response: コミュニティ作成の結果（201, 400, 409）
    """
    return service.create()


@community_bp.route("/join", methods=["POST"])
def join():
    """
    M3: コミュニティ参加処理

    Returns:
        Response: 成功時200, 不存在404
    """
    return service.join()


@community_bp.route("/leave", methods=["DELETE"])
def leave():
    """
    M4: コミュニティ脱退処理

    Returns:
        Response: 成功時200, エラー400
    """
    return service.leave()


@community_bp.route("/template_tags", methods=["POST", "PUT", "DELETE"])
def edit_tags():
    """
    M5: テンプレートタグ編集処理

    Returns:
        Response: POST=201, PUT/DELETE=200, エラー400/405
    """
    return service.edit_tags()


@community_bp.route("/template_tags", methods=["GET"])
def get_tags():
    """
    M6: テンプレートタグ取得処理

    Returns:
        Response: テンプレートタグ一覧（成功時200）
    """
    return service.get_tags()
