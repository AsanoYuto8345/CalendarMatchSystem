# C5 カレンダー情報処理部 CalenderProcessクラス 担当: 角田一颯

from flask import Blueprint, request, jsonify
from .calendar_process import CalenderProcess

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/<string:community_id>/calendar')
processor = CalenderProcess()

@calendar_bp.route('/tag/add', methods=['POST'])
def add_tag(community_id):
    data = request.get_json() or {}

    tag_name     = data.get("tag_name")
    tag_color    = data.get("tag_color")
    submitter_id = data.get("submitter_id")
    date         = data.get("date")

    if not tag_name:
        return jsonify({"error": "tag_nameが未指定です"}), 400
    if not tag_color:
        return jsonify({"error": "tag_colorが未指定です"}), 400
    if not submitter_id:
        return jsonify({"error": "submitter_idが未指定です"}), 400
    if not date:
        return jsonify({"error": "dateが未指定です"}), 400

    if not tag_name or not tag_color:
        return jsonify({"error": "tag_nameもしくはtag_colorが未指定"}), 400

    success, result = processor.tag_add(tag_name, tag_color, submitter_id, community_id, date)
    return (jsonify(result), 200) if success else (jsonify(result), 400)

@calendar_bp.route('/tag/delete', methods=['DELETE'])
def delete_tag(community_id):
    data = request.get_json()
    tag_id = data.get("tag_id")

    if not tag_id:
        return jsonify({"error": "tag_idが未指定"}), 400

    success, result = processor.tag_delete(tag_id)
    return (jsonify(result), 200) if success else (jsonify(result), 404)

@calendar_bp.route('/tag/get', methods=['GET'])
def get_community_date_tag(community_id):
    date = request.args.get("date")
    
    if not date:
        return jsonify({"error": "date未指定"}), 400
    
    success, result = processor.tag_get_from_community_and_date(community_id, date)
    return (jsonify(result), 200) if success else (jsonify(result), 500)
    
    
@calendar_bp.route('tag/get/<string:user_id>', methods=['GET'])
def get_community_date_user_id(community_id, user_id):
    date = request.args.get("date")
    
    if not date:
        return jsonify({"error": "date未指定"}), 400
    
    success, result = processor.tag_get_from_community_date_user(community_id, date, user_id)
    
    if success:
        return (jsonify(result), 200) if success else (jsonify(result), 500)