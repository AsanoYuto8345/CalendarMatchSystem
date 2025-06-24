# backend/modules/community_service/community_service.py
import logging
from flask import request, jsonify

logger = logging.getLogger(__name__)

class CommunityService:
    @staticmethod
    def community_create():
        name = request.json.get("community_name", "").strip()
        if not name:
            return jsonify({"error": "コミュニティ名が未入力です"}), 400
        if len(name) > 16:
            return jsonify({"error": "16文字以内にしてください"}), 400

        # DB操作を省略して成功レスポンスを返す（モック）
        logger.info(f"✅ コミュニティ登録: {name}")
        return jsonify({
            "result": True,
            "message": f"'{name}' を登録しました",
            "community_name": name,
            "community_id": 1
        }), 201

    @staticmethod
    def community_join():
        name = request.json.get("community_name", "").strip()
        if not name:
            return jsonify({"error": "コミュニティ名が未入力です"}), 400

        logger.info(f"🚪 コミュニティ参加: {name}")
        return jsonify({
            "result": True,
            "message": f"'{name}' に参加しました",
            "community_name": name,
            "community_id": 1
        }), 200

    @staticmethod
    def community_leave():
        user_id = request.json.get("id", "").strip()
        community_id = request.json.get("community_id", "").strip()

        if not user_id or not community_id:
            return jsonify({"error": "ID未入力です"}), 400

        return jsonify({
            "result": True,
            "message": f"ユーザ '{user_id}' はコミュニティ {community_id} を脱退しました"
        }), 200

    @staticmethod
    def edit_template_tags():
        method = request.method
        data = request.get_json() or {}
        community_id = data.get("community_id", "").strip()

        if not community_id.isdigit():
            return jsonify({"error": "無効なコミュニティIDです"}), 400

        community_id = int(community_id)
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

    @staticmethod
    def get_template_tags():
        community_id = request.args.get("community_id", "").strip()
        if not community_id.isdigit():
            return jsonify({"error": "コミュニティIDが未指定または不正です"}), 400

        tag_list = [
            {"id": 1, "tag": "予定あり"},
            {"id": 2, "tag": "重要"}
        ]
        return jsonify({"tags": tag_list}), 200
