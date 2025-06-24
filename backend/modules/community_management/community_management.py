# modules/community_management/community_management.py

"""
C9 コミュニティ情報管理部
このモジュールは疑似メモリでコミュニティ情報を管理します。
Flaskアプリケーションが再起動されるとデータは失われます。
将来的には SQLAlchemy 等の DB 永続化に差し替えることを想定しています。
"""

import logging
from flask import request, jsonify

logger = logging.getLogger(__name__)

class CommunityManagement:
    def __init__(self):
        # 疑似的な記憶領域（再起動すると消える）
        self._communities = []

    def register(self, name, image=None):
        """
        M3: コミュニティ登録処理
        重複チェックを行い、コミュニティを疑似メモリに登録する。
        """
        if name in self._communities:
            return jsonify({"error": "既に存在します"}), 409

        self._communities.append(name)
        logger.info(f"✅ コミュニティ登録: {name}")
        return jsonify({
            "result": True,
            "message": f"'{name}' を登録しました",
            "community_name": name,
            "community_id": self._communities.index(name) + 1
        }), 201

    def exists_by_name(self, name):
        """
        指定された名前のコミュニティが存在するか確認する。
        """
        return name in self._communities

    def getcommunityInfo(self):
        """
        M4: コミュニティ情報取得処理
        指定されたIDのコミュニティ情報を返却（現状は未実装）。
        """
        community_id = request.args.get("community_id", "").strip()
        if not community_id.isdigit():
            return jsonify({"error": "コミュニティIDが未指定または不正です"}), 400

        # ※本実装では ID に対応する情報は存在しないためエラーで返す
        return jsonify({"error": f"ID {community_id} のコミュニティは存在しません"}), 404

    def updatecommunityInfo(self):
        """
        M5: コミュニティ情報更新処理（未実装）
        指定されたIDの情報を更新する処理を想定。
        """
        data = request.get_json() or {}
        community_id = data.get("community_id", "").strip()

        if not community_id.isdigit():
            return jsonify({"error": "無効なコミュニティIDです"}), 400

        logger.info(f"📦 更新要求: community_id={community_id}")
        return jsonify({"result": True, "message": "コミュニティ情報を更新しました"}), 200
