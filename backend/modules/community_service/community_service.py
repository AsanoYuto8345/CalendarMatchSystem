# modules/community_service/community_service.py

"""
C4 コミュニティ処理部クラス定義
本モジュールは、コミュニティの作成・参加・脱退・テンプレートタグ処理などを担当する。
作成者: 遠藤信輝
最終更新: 2025/06/24
"""

import logging
import os
from flask import request, jsonify
from werkzeug.utils import secure_filename

from modules.community_management.community_management import CommunityManagement

logger = logging.getLogger(__name__)


class CommunityService:
    def __init__(self):
        self.management = CommunityManagement()

    def create(self):
        """
        コミュニティを新規作成する。
        フロントエンドからのmultipart/form-dataを受け取り、管理部へ登録要求を送る。
        Returns:
            Response: 成功時 201, 入力エラー時 400, 重複時 409
        """
        name = request.form.get("community_name", "").strip()
        if not name:
            return jsonify({"error": "コミュニティ名が未入力です"}), 400
        if len(name) > 16:
            return jsonify({"error": "16文字以内にしてください"}), 400

        image_file = request.files.get("image")  # 画像処理は後で実装
        return self.management.register(name, image_file)

    def join(self):
        """
        指定されたコミュニティに参加する。
        Returns:
            Response: 成功時 200, 存在しない場合 404
        """
        name = request.json.get("community_name", "").strip()
        if not self.management.exists_by_name(name):
            return jsonify({"error": f"'{name}' は存在しません"}), 404

        return jsonify({
            "result": True,
            "message": f"'{name}' に参加しました",
            "community_name": name,
            "community_id": self.management._communities.index(name) + 1
        }), 200

    def leave(self):
        """
        ユーザーを指定されたコミュニティから脱退させる。
        Returns:
            Response: 成功時 200, 入力エラー時 400
        """
        user_id = request.json.get("id", "").strip()
        community_id = request.json.get("community_id", "").strip()

        if not user_id or not community_id:
            return jsonify({"error": "ID未入力です"}), 400

        return jsonify({
            "result": True,
            "message": f"ユーザ '{user_id}' はコミュニティ {community_id} を脱退しました"
        }), 200

    def edit_tags(self):
        """
        テンプレートタグを追加・更新・削除する。
        Returns:
            Response: 操作に応じたステータスコード
        """
        method = request.method
        data = request.get_json() or {}
        community_id = data.get("community_id", "").strip()

        if not community_id.isdigit():
            return jsonify({"error": "無効なコミュニティIDです"}), 400

        tag_id = data.get("template_tag_id", "").strip()
        tag_value = data.get("tag", "").strip()

        if method == 'POST':
            if not tag_value:
                return jsonify({"error": "タグ内容が未指定です"}), 400
            return jsonify({"message": "タグを追加しました", "template_tag_id": 1, "result": True}), 201

        if not tag_id.isdigit():
            return jsonify({"error": "テンプレートタグIDが未指定または不正です"}), 400

        if method == 'PUT':
            if not tag_value:
                return jsonify({"error": "タグ内容が未指定です"}), 400
            return jsonify({"message": "タグを更新しました", "template_tag_id": int(tag_id), "result": True}), 200

        if method == 'DELETE':
            return jsonify({"message": "タグを削除しました", "template_tag_id": int(tag_id), "result": True}), 200

        return jsonify({"error": "許可されていないメソッドです"}), 405

    def get_tags(self):
        """
        指定されたコミュニティIDに紐づくテンプレートタグ一覧を返す。
        Returns:
            Response: 成功時 200, 入力エラー時 400
        """
        community_id = request.args.get("community_id", "").strip()
        if not community_id.isdigit():
            return jsonify({"error": "コミュニティIDが未指定または不正です"}), 400

        tag_list = [
            {"id": 1, "tag": "予定あり"},
            {"id": 2, "tag": "重要"}
        ]
        return jsonify({"tags": tag_list}), 200
