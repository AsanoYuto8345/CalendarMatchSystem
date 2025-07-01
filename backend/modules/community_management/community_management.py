# backend/modules/community_management/community_management.py
"""
C9 コミュニティ情報管理部
このモジュールは SQLite データベースを用いてコミュニティ情報を永続的に管理します。
"""

import logging
from flask import request, jsonify, g
import sqlite3
import os

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
    - M2: コミュニティ登録処理 [cite: 237]
    - M3: コミュニティ情報更新処理 
    - M4: コミュニティ情報取得処理 [cite: 254]
    """

    def register(self, name, image=None):
        """
        M2: コミュニティ登録処理 [cite: 243]

        Args:
            name (str): コミュニティ名（16文字以内） [cite: 245]
            image (FileStorage, optional): 画像ファイル（未使用）

        Returns:
            Response: 成功時201, 入力エラー400, 重複409 [cite: 247]
        """
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
        """
        M4: コミュニティ情報取得処理 [cite: 254]

        Returns:
            Response:
                - 成功時200:
                    {
                        "result": True,
                        "community_name": str,
                        "image_path": str or None,
                        "tags": List[str]
                    }
                - 入力エラー400 [cite: 259]
                - 存在しないID 404 [cite: 259]
        """
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
            "SELECT tag FROM template_tags WHERE community_id = ?",
            (int(community_id),)
        ).fetchall()
        tag_list = [r["tag"] for r in tag_rows]

        return jsonify({
            "result": True,
            "community_name": row["name"],
            "image_path": row["image_path"],
            "tags": tag_list
        }), 200

    def updatecommunityInfo(self):
        """
        M3: コミュニティ情報更新処理 
        指定されたコミュニティIDに紐づくテンプレートタグを更新する処理。既存のタグ一覧を取得し、
        差分に応じて追加・削除・更新を行う。 

        Returns:
            Response:
                - 成功時200: 更新成功メッセージを返却 [cite: 252]
                - 入力エラー400 [cite: 253]
                - 存在しないID 404 [cite: 253]
                - 重複データ409 [cite: 253]
        """
        data = request.get_json() or {}
        community_id_str = data.get("community_id", "").strip()
        tags = data.get("tags", [])  # 更新後のテンプレートタグ一覧 

        if not community_id_str.isdigit():
            return jsonify({"error": "無効なコミュニティIDです"}), 400 # E1 [cite: 253]
        
        community_id = int(community_id_str)
        db = get_db()

        # コミュニティの存在確認
        community_exists = db.execute(
            "SELECT id FROM communities WHERE id = ?", (community_id,)
        ).fetchone()
        if not community_exists:
            return jsonify({"error": f"ID {community_id} のコミュニティは存在しません"}), 404 # E2 [cite: 253]

        # 現在のタグを取得
        current_tags_rows = db.execute(
            "SELECT id, tag FROM template_tags WHERE community_id = ?",
            (community_id,)
        ).fetchall()
        current_tags = {row["id"]: row["tag"] for row in current_tags_rows}
        
        # 入力されたタグと既存タグの比較、更新・追加・削除
        updated_tags_list = []
        
        # 既存タグの更新と新規タグの追加
        for tag_data in tags:
            tag_id = tag_data.get("id")
            tag_name = tag_data.get("tag", "").strip()

            if not tag_name:
                return jsonify({"error": "タグ名が未入力です"}), 400 # E1
            if len(tag_name) > 20: 
                return jsonify({"error": "タグは20文字以内にしてください"}), 400 # E1

            if tag_id and tag_id in current_tags:
                if current_tags[tag_id] != tag_name:
                    db.execute(
                        "UPDATE template_tags SET tag = ? WHERE id = ? AND community_id = ?",
                        (tag_name, tag_id, community_id)
                    )
                    logger.info(f"✅ タグ更新: ID={tag_id}, Name='{tag_name}'")
                updated_tags_list.append({"id": tag_id, "tag": tag_name})
                del current_tags[tag_id]
            else:
                try:
                    cursor = db.execute(
                        "INSERT INTO template_tags (community_id, tag) VALUES (?, ?)",
                        (community_id, tag_name)
                    )
                    new_id = cursor.lastrowid
                    updated_tags_list.append({"id": new_id, "tag": tag_name})
                    logger.info(f"✅ 新規タグ追加: ID={new_id}, Name='{tag_name}'")
                except sqlite3.IntegrityError:
                    return jsonify({"error": f"タグ '{tag_name}' は既に存在します"}), 409 # E3 [cite: 234]

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
            "updated_tags": updated_tags_list # 更新後のタグ一覧を返す [cite: 252]
        }), 200