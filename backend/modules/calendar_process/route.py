# C5 カレンダー情報処理部 CalenderProcessクラス 担当: 角田 一颯

from flask import Blueprint, request, jsonify
from .calendar_process import CalenderProcess

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/<string:communityId>/calendar')
processor = CalenderProcess()

@calendar_bp.before_request
def before_request():
    community_id = request.view_args.get('communityId')

@calendar_bp.route('/tag/add', methods=['POST'])
def add_tag():
    data = request.get_json()
    tag_name = data.get("tag_name")
    tag_color = data.get("tag_color")
    if not tag_name or not tag_color:
        return jsonify({"error": "tag_nameもしくはtag_colorが未指定"}), 400

    success, result = processor.tag_add(tag_name, tag_color)
    return (jsonify(result), 200) if success else (jsonify(result), 400)

@calendar_bp.route('/tag/delete', methods=['DELETE'])
def delete_tag():
    data = request.get_json()
    tag_id = data.get("tag_id")

    if not tag_id:
        return jsonify({"error": "tag_idが未指定"}), 400

    success, result = processor.tag_delete(tag_id)
    return (jsonify(result), 200) if success else (jsonify(result), 404)
