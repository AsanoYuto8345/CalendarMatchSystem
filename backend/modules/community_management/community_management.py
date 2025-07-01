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
    - M2: コミュニティ登録処理
    - M3: コミュニティ情報更新処理（仮実装）
    - M4: コミュニティ情報取得処理
    """

    def register(self, name, image=None):
        """
        M2: コミュニティ登録処理

        Args:
            name (str): コミュニティ名（16文字以内）
            image (FileStorage, optional): 画像ファイル（未使用）

        Returns:
            Response: 成功時201, 入力エラー400, 重複409
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
        M4: コミュニティ情報取得処理

        Returns:
            Response:
                - 成功時200:
                    {
                        "result": True,
                        "community_name": str,
                        "image_path": str or None,
                        "tags": List[str]
                    }
                - 入力エラー400
                - 存在しないID 404
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
        ※ 名前や画像の更新は行わない仕様

        Returns:
            Response:
                - 成功時200: 更新成功メッセージを返却
                - 入力エラー400
        """
        data = request.get_json() or {}
        community_id = data.get("community_id", "").strip()

        if not community_id.isdigit():
            return jsonify({"error": "無効なコミュニティIDです"}), 400

        logger.info(f"📦 更新要求: community_id={community_id}")
        return jsonify({
            "result": True,
            "message": "コミュニティ情報を更新しました"
        }), 200
