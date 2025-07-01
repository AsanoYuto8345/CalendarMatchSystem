# backend/modules/community_management/community_management.py
"""
C9 コミュニティ情報管理部
このモジュールは SQLite データベースを用いてコミュニティ情報を永続的に管理します。
"""

import logging
from flask import request, jsonify, g
import sqlite3
import os
import re

logger = logging.getLogger(__name__)

# SQLite ファイルのパス
DB_PATH = os.path.join(os.path.dirname(__file__), "../../instance/messages.db")


def get_db():
    """
    SQLite 接続を取得する（Flask の g オブジェクトにバインド）

    Returns:
        sqlite3.Connection: データベース接続
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """
    SQLite 接続をクローズする
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """
    SQLite データベース初期化（テーブルがなければ作成）
    """
    db = sqlite3.connect(DB_PATH)
    db.execute("""
        CREATE TABLE IF NOT EXISTS communities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            image_path TEXT
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS template_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            community_id INTEGER NOT NULL,
            tag TEXT NOT NULL,
            color_code TEXT NOT NULL,
            FOREIGN KEY (community_id) REFERENCES communities(id)
        )
    """)
    db.commit()
    db.close()


# 初期化呼び出し
init_db()


class CommunityManagement:
    """
    C9 コミュニティ情報管理部 管理クラス
    - M2: コミュニティ登録処理
    - M3: コミュニティ情報更新処理 
    - M4: コミュニティ情報取得処理
    """

    def register(self, name, image=None):
        if not name:
            return jsonify({"error": "コミュニティ名が未入力です"}), 400
        if len(name) > 16:
            return jsonify({"error": "16文字以内にしてください"}), 400

        db = get_db()
        try:
            db.execute("INSERT INTO communities (name) VALUES (?)", (name,))
            db.commit()
        except sqlite3.IntegrityError:
            return jsonify({"error": "既に存在します"}), 409

        community_id = db.execute(
            "SELECT id FROM communities WHERE name = ?", (name,)
        ).fetchone()["id"]

        logger.info(f"✅ コミュニティ登録: {name}")
        return jsonify({
            "result": True,
            "message": f"'{name}' を登録しました",
            "community_name": name,
            "community_id": community_id
        }), 201

    def getcommunityInfo(self):
        community_id = request.args.get("community_id", "").strip()

        if not community_id.isdigit():
            return jsonify({"error": "コミュニティIDが未指定または不正です"}), 400

        db = get_db()
        row = db.execute(
            "SELECT name, image_path FROM communities WHERE id = ?",
            (int(community_id),)
        ).fetchone()

        if not row:
            return jsonify({"error": f"ID {community_id} のコミュニティは存在しません"}), 404

        tag_rows = db.execute(
            "SELECT tag, color_code FROM template_tags WHERE community_id = ?",
            (int(community_id),)
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
        community_id_str = data.get("community_id", "").strip()
        tags = data.get("tags", [])

        if not community_id_str.isdigit():
            return jsonify({"error": "無効なコミュニティIDです"}), 400
        community_id = int(community_id_str)
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
            color_code = tag_data.get("colorCode", "#000000").strip()

            if not tag_name:
                return jsonify({"error": "タグ名が未入力です"}), 400
            if len(tag_name) > 20:
                return jsonify({"error": "タグは20文字以内にしてください"}), 400
            if not re.fullmatch(r"^#[0-9a-fA-F]{6}$", color_code):
                color_code = "#000000"

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
                try:
                    cursor = db.execute(
                        "INSERT INTO template_tags (community_id, tag, color_code) VALUES (?, ?, ?)",
                        (community_id, tag_name, color_code)
                    )
                    new_id = cursor.lastrowid
                    updated_tags_list.append({"id": new_id, "tag": tag_name, "colorCode": color_code})
                    logger.info(f"✅ 新規タグ追加: ID={new_id}, Name='{tag_name}'")
                except sqlite3.IntegrityError:
                    return jsonify({"error": f"タグ '{tag_name}' は既に存在します"}), 409

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