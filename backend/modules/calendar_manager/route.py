# C10 カレンダー情報管理部ルーティング  担当: 角田 一颯

from flask import Blueprint, request, jsonify
# app.pyで初期化されたdbインスタンスとTagモデルをインポート
# app.pyが親ディレクトリにあるため、相対インポートを使用
from ..app import db # app.pyからdbインスタンスをインポート
from .calendar_manager import CalendarManager, Tag # CalendarManagerとTagモデルをインポート

calendar_manager_bp = Blueprint('calendar_manager', __name__, url_prefix='/api/calendar-manager')
# CalendarManagerインスタンスを初期化する際に、app.pyで初期化されたdbインスタンスを渡す
manager = CalendarManager(db)

@calendar_manager_bp.route('/tag/add', methods=['POST'])
def manager_tag_add():
    """
    C10 M1 カレンダー情報管理主処理 - タグ追加 APIエンドポイント
    """
    data = request.get_json()
    if not data:
        return jsonify({"result": False, "message": "リクエストボディが空です。"}), 400

    tag_id = data.get("tag_id")
    tag_name = data.get("tag_name")

    if not tag_id:
        return jsonify({"result": False, "message": "tag_idが未指定です。"}), 400
    if not tag_name:
        return jsonify({"result": False, "message": "tag_nameが未指定です。"}), 400

    result = manager.tag_add(tag_id, tag_name)
    if result["result"]:
        return jsonify(result), 200
    else:
        status_code = 400 if "既に存在" in result["message"] else 500
        return jsonify(result), status_code

@calendar_manager_bp.route('/tag/delete', methods=['POST'])
def manager_tag_delete():
    """
    C10 M1 カレンダー情報管理主処理 - タグ削除 APIエンドポイント
    """
    data = request.get_json()
    if not data:
        return jsonify({"result": False, "message": "リクエストボディが空です。"}), 400

    tag_id = data.get("tag_id")
    tag_name = data.get("tag_name")

    if not tag_id:
        return jsonify({"result": False, "message": "tag_idが未指定です。"}), 400
    if not tag_name:
        return jsonify({"result": False, "message": "tag_nameが未指定です。"}), 400

    result = manager.tag_delete(tag_id, tag_name)
    if result["result"]:
        return jsonify(result), 200
    else:
        status_code = 404 if "見つかりません" in result["message"] else 500
        return jsonify(result), status_code

@calendar_manager_bp.route('/tag/edit', methods=['POST'])
def manager_tag_edit():
    """
    C10 M1 カレンダー情報管理主処理 - タグ編集 APIエンドポイント
    """
    data = request.get_json()
    if not data:
        return jsonify({"result": False, "message": "リクエストボディが空です。"}), 400

    tag_id = data.get("tag_id")
    new_tag_name = data.get("new_tag_name")

    if not tag_id:
        return jsonify({"result": False, "message": "tag_idが未指定です。"}), 400
    if not new_tag_name:
        return jsonify({"result": False, "message": "new_tag_nameが未指定です。"}), 400

    result = manager.tag_edit(tag_id, new_tag_name)
    if result["result"]:
        return jsonify(result), 200
    else:
        status_code = 404 if "見つかりません" in result["message"] else (409 if "既に他のタグ" in result["message"] else 500)
        return jsonify(result), status_code

@calendar_manager_bp.route('/tags', methods=['GET'])
def manager_get_all_tags():
    """
    C10 M1 カレンダー情報管理主処理 - 全タグ取得 APIエンドポイント
    """
    result = manager.get_all_tags()
    if result["result"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500