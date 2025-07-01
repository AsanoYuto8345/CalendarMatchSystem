#backend/modules/community_service/community_service.py
"""
C4 コミュニティ処理部クラス定義
本モジュールは、コミュニティの作成・参加・脱退・テンプレートタグ処理などを担当する。
作成者: 遠藤信輝
最終更新: 2025/06/26
"""

import logging
import re
from flask import request, jsonify
from werkzeug.utils import secure_filename

from modules.community_management.community_management import get_db

logger = logging.getLogger(__name__)


class CommunityService:
    """
    コミュニティ関連の操作を提供するサービスクラス。
    """

    def create(self):
        """
        コミュニティを新規作成する。

        Returns:
            Response: 成功時201, 入力エラー時400, 重複時409
        """
        name = request.form.get("community_name", "").strip()
        if not name:
            return jsonify({"error": "コミュニティ名が未入力です"}), 400
        if len(name) > 16:
            return jsonify({"error": "16文字以内にしてください"}), 400

        image_file = request.files.get("image")
        image_path = None

        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            image_path = f"uploads/{filename}"
            image_file.save(image_path)
            logger.info(f"🖼️ 画像保存: {image_path}")

        db = get_db()
        try:
            db.execute(
                "INSERT INTO communities (name, image_path) VALUES (?, ?)",
                (name, image_path)
            )
            db.commit()
        except Exception as e:
            logger.warning(f"❌ コミュニティ作成失敗: {e}")
            return jsonify({"error": "既に存在します"}), 409

        community_id = db.execute(
            "SELECT id FROM communities WHERE name = ?", (name,)
        ).fetchone()["id"]

        return jsonify({
            "result": True,
            "message": f"'{name}' を登録しました",
            "community_name": name,
            "community_id": community_id
        }), 201

    def join(self):
        """
        指定されたコミュニティに参加する。

        Returns:
            Response: 成功時200, 不存在404
        """
        name = request.json.get("community_name", "").strip()
        db = get_db()
        row = db.execute(
            "SELECT id FROM communities WHERE name = ?", (name,)
        ).fetchone()

        if not row:
            return jsonify({"error": f"'{name}' は存在しません"}), 404

        return jsonify({
            "result": True,
            "message": f"'{name}' に参加しました",
            "community_name": name,
            "community_id": row["id"]
        }), 200

    def leave(self):
        """
        ユーザーを指定されたコミュニティから脱退させる（処理は仮実装）。

        Returns:
            Response: 成功時200, 入力エラー時400
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
            Response: 操作に応じて201/200/400/404など
        """
        method = request.method
        data = request.get_json() or {}
        community_id = data.get("community_id", "").strip()

        if not community_id.isdigit():
            return jsonify({"error": "無効なコミュニティIDです"}), 400

        db = get_db()

        if method == 'POST':
            tag_value = data.get("tag", "").strip()
            color_code = data.get("colorCode", "#000000").strip()

            if not tag_value:
                return jsonify({"error": "タグ内容が未指定です"}), 400

            if not re.fullmatch(r"^#[0-9a-fA-F]{6}$", color_code):
                color_code = "#000000"

            db.execute(
                "INSERT INTO template_tags (community_id, tag, color_code) VALUES (?, ?, ?)",
                (int(community_id), tag_value, color_code)
            )
            db.commit()

            new_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

            return jsonify({
                "message": "タグを追加しました",
                "template_tag_id": new_id,
                "color_code": color_code,
                "result": True
            }), 201

        tag_id = data.get("template_tag_id", "").strip()
        if not tag_id.isdigit():
            return jsonify({"error": "テンプレートタグIDが未指定または不正です"}), 400

        if method == 'PUT':
            tag_value = data.get("tag", "").strip()
            color_code = data.get("colorCode", "#000000").strip()

            if not tag_value:
                return jsonify({"error": "タグ内容が未指定です"}), 400

            if not re.fullmatch(r"^#[0-9a-fA-F]{6}$", color_code):
                color_code = "#000000"

            db.execute(
                "UPDATE template_tags SET tag = ?, color_code = ? WHERE id = ? AND community_id = ?",
                (tag_value, color_code, int(tag_id), int(community_id))
            )
            db.commit()

            return jsonify({
                "message": "タグを更新しました",
                "template_tag_id": int(tag_id),
                "color_code": color_code,
                "result": True
            }), 200

        if method == 'DELETE':
            db.execute(
                "DELETE FROM template_tags WHERE id = ? AND community_id = ?",
                (int(tag_id), int(community_id))
            )
            db.commit()

            return jsonify({
                "message": "タグを削除しました",
                "template_tag_id": int(tag_id),
                "result": True
            }), 200

        return jsonify({"error": "許可されていないメソッドです"}), 405

    def get_tags(self):
        """
        指定されたコミュニティIDに紐づくテンプレートタグ一覧を返す。

        Returns:
            Response: 成功時200, 入力エラー時400
        """
        community_id = request.args.get("community_id", "").strip()
        if not community_id.isdigit():
            return jsonify({"error": "コミュニティIDが未指定または不正です"}), 400

        db = get_db()
        rows = db.execute(
            "SELECT id, tag, color_code FROM template_tags WHERE community_id = ?",
            (int(community_id),)
        ).fetchall()

        tag_list = [
            {"id": row["id"], "tag": row["tag"], "color_code": row["color_code"] or "#000000"}
            for row in rows
        ]

        return jsonify({"tags": tag_list}), 200
