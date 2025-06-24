# C5 カレンダー情報処理部 CalenderProcessクラス 担当: 角田 一颯

from flask import Blueprint, request, jsonify
from .calendarprocess import CalenderProcess

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/calendar')
processor = CalenderProcess()

@calendar_bp.route('/tag/add', methods=['POST'])
def add_tag():
    data = request.get_json()
    tag_name = data.get("tag_name")

    if not tag_name:
        return jsonify({"error": "tag_nameが未指定"}), 400

    success, result = processor.tag_add(tag_name)
    return (jsonify(result), 200) if success else (jsonify(result), 400)

@calendar_bp.route('/tag/delete', methods=['POST'])
def delete_tag():
    data = request.get_json()
    tag_id = data.get("tag_id")
    tag_name = data.get("tag_name")

    if not tag_id or not tag_name:
        return jsonify({"error": "tag_idまたはtag_nameが未指定"}), 400

    success, result = processor.tag_delete(tag_id, tag_name)
    return (jsonify(result), 200) if success else (jsonify(result), 404)
