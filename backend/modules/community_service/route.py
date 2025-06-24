# modules/community_service/route.py

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

@community_bp.route("/create", methods=["POST"])
def create():
    """
    M2: コミュニティ作成処理
    フォームデータ形式で名称と画像を受け取り、作成を行う。
    """
    return service.create()

@community_bp.route("/join", methods=["POST"])
def join():
    """
    M3: コミュニティ参加処理
    JSONで指定されたコミュニティ名に対して参加を試みる。
    """
    return service.join()

@community_bp.route("/leave", methods=["DELETE"])
def leave():
    """
    M4: コミュニティ脱退処理
    ユーザIDとコミュニティIDを指定して脱退処理を行う。
    """
    return service.leave()

@community_bp.route("/template_tags", methods=["POST", "PUT", "DELETE"])
def edit_tags():
    """
    M5: テンプレートタグ編集処理
    タグの新規作成、更新、削除を行う。
    """
    return service.edit_tags()

@community_bp.route("/template_tags", methods=["GET"])
def get_tags():
    """
    M6: テンプレートタグ取得処理
    指定されたコミュニティIDに紐づくテンプレートタグ一覧を返す。
    """
    return service.get_tags()
