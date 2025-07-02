# modules/calendar_manager/matching_route.py

from flask import Blueprint, request, jsonify
from .matching import Matching

matching_bp = Blueprint('matching', __name__, url_prefix='/api/matching')
matching = Matching()

@matching_bp.route('/', methods=['GET'])
def request_matching():
    """
    C6 マッチング処理要求

    Request Body (JSON):
        - community_id (str):       コミュニティID
        - tag_name (str):           タグ名
        - date (str):               日付（'YYYY-MM-DD'形式）
        - registered_user_id (str): 登録ユーザーのID

    Returns:
        flask.Response: JSONレスポンスとステータスコード
            - 200: {'result': True, 'submitter_ids': […]}
            - 400: {'result': False, 'message': "<キー>が未指定です。"}
    """
    data = request.get_json() or {}

    community_id        = data.get('community_id')
    tag_name            = data.get('tag_name')
    date                = data.get('date')
    registered_user_id  = data.get('registered_user_id')

    # 必須チェック
    missing = [k for k, v in [
        ('community_id',        community_id),
        ('tag_name',            tag_name),
        ('date',                date),
        ('registered_user_id',  registered_user_id)
    ] if not v]
    if missing:
        return jsonify({
            "result": False,
            "message": f"{', '.join(missing)} が未指定です。"
        }), 400

    # Matching クラス呼び出し
    matching_user_ids = matching.find_matching_user(
        community_id, tag_name, date, registered_user_id
    )

    return jsonify({
        "result": True,
        "matching_user_ids": matching_user_ids
    }), 200