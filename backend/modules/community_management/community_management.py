"""
C9 コミュニティ情報管理部
このモジュールは SQLite データベースを用いてコミュニティ情報・テンプレートタグ・チャットデータを永続的に管理します。
"""

import logging
from flask import request, jsonify, g
import sqlite3
import os
import re
import datetime
import uuid

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "../../instance/messages.db")

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DB_PATH)
    # communities: UUID文字列を主キーとする
    db.execute("""
        CREATE TABLE IF NOT EXISTS communities (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            image_path TEXT
        )
    """)
    # template_tags: UUID文字列を主キーとし、community_idもTEXT
    db.execute("""
        CREATE TABLE IF NOT EXISTS template_tags (
            id TEXT PRIMARY KEY,
            community_id TEXT NOT NULL,
            tag TEXT NOT NULL,
            color_code TEXT NOT NULL,
            FOREIGN KEY (community_id) REFERENCES communities(id)
        )
    """)
      # members テーブル（モデルに合わせて id を主キーにした文字列型）
    db.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            community_id TEXT NOT NULL,
            FOREIGN KEY (community_id) REFERENCES communities(id)
        )
    """)
    # chat_messages: UUID文字列を主キー、community_id/tag_idはTEXT
    db.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id TEXT PRIMARY KEY,
            community_id TEXT NOT NULL,
            tag_id TEXT NOT NULL,
            date TEXT NOT NULL,
            sender_id TEXT NOT NULL,
            message_content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (community_id) REFERENCES communities(id),
            FOREIGN KEY (tag_id)       REFERENCES template_tags(id)
        )
    """)
    db.commit()
    db.close()

init_db()

class CommunityManagement:
    """
    M1: コミュニティ情報主処理
    ユーザIDをもとに所属コミュニティとテンプレートタグ情報を検索・返却する。
    """

    def get_communities_and_tags_by_user(self, user_id):
        user_id = user_id.strip()
        if not user_id:
            return jsonify({"error": "ユーザIDが未指定です"}), 400  # E1

        db = get_db()
        rows = db.execute("""
            SELECT c.id AS community_id, c.name AS community_name, c.image_path
            FROM communities c
            INNER JOIN members m ON c.id = m.community_id
            WHERE m.user_id = ?
        """, (user_id,)).fetchall()

        result = []
        for row in rows:
            tag_rows = db.execute(
                "SELECT id, tag, color_code FROM template_tags WHERE community_id = ?",
                (row["community_id"],)
            ).fetchall()
            tags = [
                {"id": r["id"], "tag": r["tag"], "color_code": r["color_code"]} for r in tag_rows
            ]
            result.append({
                "id": user_id,
                "community_name": row["community_name"],
                "tags": tags
            })

        return jsonify({"result": True, "communities": result}), 200

    def register(self, name, image=None):
        if not name:
            return jsonify({"error": "コミュニティ名が未入力です"}), 400
        if len(name) > 16:
            return jsonify({"error": "16文字以内にしてください"}), 400

        db = get_db()
        # UUID を生成して INSERT
        community_id = uuid.uuid4().hex
        try:
            db.execute(
                "INSERT INTO communities (id, name) VALUES (?, ?)",
                (community_id, name)
            )
            db.commit()
        except sqlite3.IntegrityError:
            return jsonify({"error": "既に存在します"}), 409

        logger.info(f"✅ コミュニティ登録: {name}")
        return jsonify({
            "result": True,
            "message": f"'{name}' を登録しました",
            "community_name": name,
            "community_id": community_id
        }), 201

    def getcommunityInfo(self):
        community_id = request.args.get("community_id", "").strip()

        if not community_id:
            return jsonify({"error": "コミュニティIDが未指定または不正です"}), 400

        db = get_db()
        row = db.execute(
            "SELECT name, image_path FROM communities WHERE id = ?",
            (community_id,)
        ).fetchone()

        if not row:
            return jsonify({"error": f"ID {community_id} のコミュニティは存在しません"}), 404

        tag_rows = db.execute(
            "SELECT tag, color_code FROM template_tags WHERE community_id = ?",
            (community_id,)
        ).fetchall()
        tag_list = [{"tag": r["tag"], "colorCode": r["color_code"]} for r in tag_rows]

        return jsonify({
            "result": True,
            "community_name": row["name"],
            "image_path": row["image_path"],
            "tags": tag_list
        }), 200

    def updatecommunityInfo(self):
        data = request.get_json() or {}
        community_id = data.get("community_id", "").strip()
        tags = data.get("tags", [])

        if not community_id:
            return jsonify({"error": "無効なコミュニティIDです"}), 400

        db = get_db()
        community_exists = db.execute(
            "SELECT id FROM communities WHERE id = ?", (community_id,)
        ).fetchone()
        if not community_exists:
            return jsonify({"error": f"ID {community_id} のコミュニティは存在しません"}), 404

        current_tags_rows = db.execute(
            "SELECT id, tag FROM template_tags WHERE community_id = ?",
            (community_id,)
        ).fetchall()
        current_tags = {row["id"]: row["tag"] for row in current_tags_rows}

        updated_tags_list = []

        for tag_data in tags:
            tag_id = tag_data.get("id")
            tag_name = tag_data.get("tag", "").strip()
            color_code = tag_data.get("colorCode", "000000").strip()

            if not tag_name:
                return jsonify({"error": "タグ名が未入力です"}), 400
            if len(tag_name) > 20:
                return jsonify({"error": "タグは20文字以内にしてください"}), 400
            if not re.fullmatch(r"^#[0-9a-fA-F]{6}$", color_code):
                color_code = "000000"

            if tag_id and tag_id in current_tags:
                if current_tags[tag_id] != tag_name:
                    db.execute(
                        "UPDATE template_tags SET tag = ?, color_code = ? WHERE id = ? AND community_id = ?",
                        (tag_name, color_code, tag_id, community_id)
                    )
                    logger.info(f"✅ タグ更新: ID={tag_id}, Name='{tag_name}'")
                updated_tags_list.append({"id": tag_id, "tag": tag_name, "colorCode": color_code})
                del current_tags[tag_id]
            else:
                new_id = uuid.uuid4().hex
                db.execute(
                    "INSERT INTO template_tags (id, community_id, tag, color_code) VALUES (?, ?, ?, ?)",
                    (new_id, community_id, tag_name, color_code)
                )
                logger.info(f"✅ 新規タグ追加: ID={new_id}, Name='{tag_name}'")
                updated_tags_list.append({"id": new_id, "tag": tag_name, "colorCode": color_code})

        for tag_id_to_delete in current_tags.keys():
            db.execute(
                "DELETE FROM template_tags WHERE id = ? AND community_id = ?",
                (tag_id_to_delete, community_id)
            )
            logger.info(f"✅ タグ削除: ID={tag_id_to_delete}")

        db.commit()

        return jsonify({
            "result": True,
            "message": "コミュニティ情報を更新しました",
            "updated_tags": updated_tags_list
        }), 200

    def post_chat(self, community_id, tag_id, data):
        date = data.get("date", "").strip()
        message = data.get("message", "").strip()
        sender_id = data.get("sender_id", "").strip()

        if not all([community_id, tag_id, date, message, sender_id]):
            return jsonify({"post_status": False, "error": "必要な項目が不足しています。"}), 400

        db = get_db()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            new_id = uuid.uuid4().hex
            db.execute(
                """
                INSERT INTO chat_messages
                  (id, community_id, tag_id, date, sender_id, message_content, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (new_id, community_id, tag_id, date, sender_id, message, timestamp)
            )
            db.commit()
        except Exception as e:
            logger.warning(f"❌ チャット保存失敗: {e}")
            return jsonify({"post_status": False, "error": "メッセージ保存中にエラーが発生しました。"}), 500

        new_message = {
            "sender_id": sender_id,
            "sender_name": sender_id,
            "message_content": message,
            "timestamp": timestamp
        }
        return jsonify({"post_status": True, "new_message": new_message}), 201

    def get_chat_history(self, community_id, tag_id, date):
        if not all([community_id, tag_id, date]):
            return jsonify({"error": "不正な入力です"}), 400

        db = get_db()
        try:
            rows = db.execute(
                """
                SELECT sender_id, message_content, timestamp
                FROM chat_messages
                WHERE community_id = ? AND tag_id = ? AND date = ?
                ORDER BY timestamp ASC
                """,
                (community_id, tag_id, date)
            ).fetchall()
        except Exception as e:
            logger.warning(f"❌ チャット履歴取得失敗: {e}")
            return jsonify({"error": "チャット履歴の取得に失敗しました。"}), 500

        chat_history = [
            {
                "sender_id": row["sender_id"],
                "sender_name": row["sender_id"],
                "message_content": row["message_content"],
                "timestamp": row["timestamp"]
            } for row in rows
        ]

        return jsonify({"chat_history": chat_history}), 200

    def get_community_members(self, community_id):
        if not community_id:
            return jsonify({"error": "無効なコミュニティIDです"}), 400

        db = get_db()
        community_exists = db.execute(
            "SELECT 1 FROM communities WHERE id = ?", (community_id,)
        ).fetchone()
        if not community_exists:
            return jsonify({"error": f"ID {community_id} のコミュニティは存在しません"}), 404

        members = db.execute(
            "SELECT user_id FROM members WHERE community_id = ?",
            (community_id,)
        ).fetchall()

        member_list = [row["user_id"] for row in members]

        return jsonify({"result": True, "members": member_list}), 200

    def get_template_tag_info_by_id(self, template_tag_id):
        if not template_tag_id:
            return jsonify({"error": "テンプレートタグIDが未入力です"})
        
        db = get_db()
        template_tag = db.execute(
            "SELECT id, tag, color_code, community_id FROM template_tags WHERE id = ?",
            (template_tag_id,)
        ).fetchone()
        
        if not template_tag:
            return jsonify({"error": f"ID {template_tag_id} のテンプレートタグは存在しません"}), 404
        
        template_tag = {
            "id": template_tag["id"],
            "tag": template_tag["tag"],
            "color_code": template_tag["color_code"],
            "community_id": template_tag["community_id"]
        }
        
        return jsonify({"result": True, "template_tag": template_tag})