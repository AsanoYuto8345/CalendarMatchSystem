"""
C4 コミュニティ処理部クラス定義
本モジュールは、コミュニティの作成・参加・脱退・テンプレートタグ処理、チャット処理などを担当する。
作成者: 遠藤信輝
最終更新: 2025/07/01
"""

import logging
import datetime
import os
import re
import uuid
from flask import request, jsonify
from werkzeug.utils import secure_filename

from modules.community_management.community_management import get_db, CommunityManagement

logger = logging.getLogger(__name__)
UPLOAD_ROOT = "uploads"

class CommunityService:
    """
    コミュニティ関連の操作を提供するサービスクラス。
    """

    def create(self):
        """
        M2 新しいコミュニティを作成し、必要に応じて画像ファイルを保存する。
        """
        name = request.form.get("community_name", "").strip()
        if not name:
            return jsonify({"error": "コミュニティ名が未入力です"}), 400
        if len(name) > 16:
            return jsonify({"error": "16文字以内にしてください"}), 400

        image_file = request.files.get("image")
        image_path = None
        db = get_db()

        # UUID文字列を生成してコミュニティを登録
        new_id = uuid.uuid4().hex
        try:
            db.execute(
                "INSERT INTO communities (id, name) VALUES (?, ?)",
                (new_id, name)
            )
            db.commit()
        except Exception as e:
            logger.warning(f"❌ コミュニティ作成失敗: {e}")
            return jsonify({"error": "既に存在します"}), 409

        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            community_folder = os.path.join(UPLOAD_ROOT, new_id)
            os.makedirs(community_folder, exist_ok=True)
            image_path = os.path.join(community_folder, filename)
            image_file.save(image_path)
            logger.info(f"🖼️ 画像保存: {image_path}")

            db.execute(
                "UPDATE communities SET image_path = ? WHERE id = ?",
                (image_path, new_id)
            )
            db.commit()

        return jsonify({
            "result": True,
            "message": f"'{name}' を登録しました",
            "community_name": name,
            "community_id": new_id,
            "image_path": image_path
        }), 201

    def join(self):
        """
        M3 指定されたユーザを既存のコミュニティに参加させる。
        """
        data = request.get_json() or {}
        name = data.get("community_name", "").strip()
        user_id = data.get("user_id", "").strip()
        if not user_id:
            return jsonify({"error": "ユーザーIDが未指定です"}), 400

        db = get_db()
        row = db.execute(
            "SELECT id FROM communities WHERE name = ?", (name,)
        ).fetchone()
        if not row:
            return jsonify({"error": f"'{name}' は存在しません"}), 404

        community_id = row["id"]
        # UUID文字列を生成して参加履歴を登録
        member_id = uuid.uuid4().hex
        try:
            db.execute(
                "INSERT INTO members (id, user_id, community_id) VALUES (?, ?, ?)",
                (member_id, user_id, community_id)
            )
            db.commit()
        except Exception as e:
            logger.warning(f"❌ 参加処理失敗: {e}")
            return jsonify({"error": "参加処理中にエラーが発生しました"}), 500

        return jsonify({
            "result": True,
            "message": f"'{name}' に参加しました",
            "community_name": name,
            "community_id": community_id
        }), 200

    def get_joined_communities(self):
        """
        M9 指定されたユーザが所属している全てのコミュニティ情報を取得する。
        """
        user_id = request.args.get("user_id", "").strip()
        if not user_id:
            return jsonify({"error": "ユーザIDが未指定です"}), 400

        db = get_db()
        rows = db.execute(
            """
            SELECT c.id, c.name, c.image_path
            FROM communities c
            INNER JOIN members m ON c.id = m.community_id
            WHERE m.user_id = ?
            """, (user_id,)
        ).fetchall()

        communities = [
            {
                "id": row["id"],
                "name": row["name"],
                "iconUrl": f"/{row['image_path']}" if row["image_path"] else "/icons/default.png"
            }
            for row in rows
        ]
        return jsonify({"communities": communities}), 200

    def leave(self):
        """
        M4 指定されたユーザをコミュニティから脱退させる。
        """
        data = request.get_json() or {}
        user_id = data.get("user_id", "").strip()
        community_id = data.get("community_id", "").strip()
        if not user_id or not community_id:
            return jsonify({"error": "ID未入力です"}), 400

        db = get_db()
        db.execute(
            "DELETE FROM members WHERE user_id = ? AND community_id = ?",
            (user_id, community_id)
        )
        db.commit()
        return jsonify({
            "result": True,
            "message": f"ユーザ '{user_id}' はコミュニティ {community_id} を脱退しました"
        }), 200

    def edit_tags(self):
        """
        M5 テンプレートタグの追加・更新・削除を実行する。
        """
        method = request.method
        data = request.get_json() or {}
        community_id = data.get("community_id", "").strip()
        if not community_id:
            return jsonify({"error": "無効なコミュニティIDです"}), 400

        db = get_db()
        if method == 'POST':
            tag_value = data.get("tag", "").strip()
            color_code = data.get("colorCode", "000000").strip()
            if not tag_value:
                return jsonify({"error": "タグ内容が未指定です"}), 400
            if not re.fullmatch(r"^[0-9a-fA-F]{6}$", color_code):
                color_code = "000000"
            new_id = uuid.uuid4().hex
            db.execute(
                "INSERT INTO template_tags (id, community_id, tag, color_code) VALUES (?, ?, ?, ?)",
                (new_id, community_id, tag_value, color_code)
            )
            db.commit()
            return jsonify({
                "message": "タグを追加しました",
                "template_tag_id": new_id,
                "color_code": color_code,
                "result": True
            }), 201

        tag_id = data.get("template_tag_id", "").strip()
        if not tag_id:
            return jsonify({"error": "テンプレートタグIDが未指定または不正です"}), 400

        if method == 'PUT':
            tag_value = data.get("tag", "").strip()
            color_code = data.get("colorCode", "000000").strip()
            if not tag_value:
                return jsonify({"error": "タグ内容が未指定です"}), 400
            if not re.fullmatch(r"^[0-9a-fA-F]{6}$", color_code):
                color_code = "000000"
            db.execute(
                "UPDATE template_tags SET tag = ?, color_code = ? WHERE id = ? AND community_id = ?",
                (tag_value, color_code, tag_id, community_id)
            )
            db.commit()
            return jsonify({
                "message": "タグを更新しました",
                "template_tag_id": tag_id,
                "color_code": color_code,
                "result": True
            }), 200

        if method == 'DELETE':
            db.execute(
                "DELETE FROM template_tags WHERE id = ? AND community_id = ?",
                (tag_id, community_id)
            )
            db.commit()
            return jsonify({
                "message": "タグを削除しました",
                "template_tag_id": tag_id,
                "result": True
            }), 200

        return jsonify({"error": "許可されていないメソッドです"}), 405

    def get_tags(self):
        """
        M6 指定されたコミュニティIDに対応するテンプレートタグの一覧を取得する。
        """
        community_id = request.args.get("community_id", "").strip()
        if not community_id:
            return jsonify({"error": "コミュニティIDが未指定です"}), 400
        db = get_db()
        rows = db.execute(
            "SELECT id, tag, color_code FROM template_tags WHERE community_id = ?",
            (community_id,)
        ).fetchall()
        tag_list = [
            {"id": row["id"], "tag": row["tag"], "color_code": row["color_code"] or "000000"}
            for row in rows
        ]
        return jsonify({"tags": tag_list}), 200

    def post_chat(self, community_id, tag_id):
        """
        M8 チャットメッセージをデータベースに登録する。
        """
        data = request.get_json() or {}
        date = data.get("date", "").strip()
        message = data.get("message", "").strip()
        sender_id = data.get("sender_id", "").strip()
        if not all([community_id, tag_id, date, message, sender_id]):
            return jsonify({"post_status": False, "error": "必要な項目が不足しています。"}), 400
        if len(message) > 200:
            return jsonify({"post_status": False, "error": "半角英数字200文字以内で入力してください。"}), 400
        db = get_db()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_id = uuid.uuid4().hex
        try:
            db.execute(
                "INSERT INTO chat_messages (id, community_id, tag_id, date, sender_id, message_content, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (new_id, community_id, tag_id, date, sender_id, message, timestamp)
            )
            db.commit()
        except Exception as e:
            logger.warning(f"❌ チャット保存失敗: {e}")
            return jsonify({"post_status": False, "error": "メッセージ保存中にエラーが発生しました。"}), 500
        new_message = {"sender_id": sender_id, "sender_name": sender_id, "message_content": message, "timestamp": timestamp}
        return jsonify({"post_status": True, "new_message": new_message}), 201

    def get_chat_history(self, community_id, tag_id):
        """
        M9 指定されたコミュニティ・タグ・日付に紐づくチャット履歴を取得する。
        """
        date = request.args.get("date", "").strip()
        if not all([community_id, tag_id, date]):
            return jsonify({"error": "不正な入力です"}), 400
        db = get_db()
        try:
            rows = db.execute(
                "SELECT sender_id, message_content, timestamp FROM chat_messages WHERE community_id = ? AND tag_id = ? AND date = ? ORDER BY timestamp ASC",
                (community_id, tag_id, date)
            ).fetchall()
        except Exception as e:
            logger.warning(f"❌ チャット履歴取得失敗: {e}")
            return jsonify({"error": "チャット履歴の取得に失敗しました。"}), 500
        chat_history = [{"sender_id": r["sender_id"], "sender_name": r["sender_id"], "message_content": r["message_content"], "timestamp": r["timestamp"]} for r in rows]
        return jsonify({"chat_history": chat_history}), 200

    def get_community_members(self):
        """
        M7: 指定されたコミュニティIDに所属するユーザ一覧を取得する。
        """
        community_id = request.args.get("community_id", "").strip()
        if not community_id:
            return jsonify({"error": "コミュニティIDが未指定です"}), 400
        from modules.community_management.community_management import CommunityManagement
        return CommunityManagement().get_community_members(community_id)

    def get_community_info_by_id(self):
        """
        M10: コミュニティIDから情報取得
        """
        community_id = request.args.get("community_id", "").strip()
        from modules.community_management.community_management import CommunityManagement
        cm = CommunityManagement()
        return cm.get_community_info_by_id(community_id)

    def get_community_info_by_tag_id(self):
        """
        M11: テンプレートタグIDからコミュニティ情報取得
        """
        tag_id = request.args.get("tag_id", "").strip()
        from modules.community_management.community_management import CommunityManagement
        cm = CommunityManagement()
        return cm.get_community_info_by_tag_id(tag_id)

    def get_template_tag_info_by_id(self):
        """
        M12: テンプレートタグIDからテンプレートタグ情報
        """
        tag_id = request.args.get("tag_id", "").strip()
        cm = CommunityManagement()
        return cm.get_template_tag_info_by_id(tag_id)
