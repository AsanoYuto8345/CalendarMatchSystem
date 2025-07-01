# C10 カレンダー情報管理部ルーティング  担当: 角田 一颯 浅野勇翔

from flask import Blueprint, request, jsonify

from extentions import db # app.pyからdbインスタンスをインポート
from .calendar_manager import CalendarManager # CalendarManagerとTagモデルをインポート

calendar_manager_bp = Blueprint('calendar_manager', __name__, url_prefix='/api/calendar-manager')
# CalendarManagerインスタンスを初期化する際に、app.pyで初期化されたdbインスタンスを渡す
manager = CalendarManager(db)


@calendar_manager_bp.route('/tags', methods=['GET'])
def manager_get_calendar_tags():
    """
    C10 M2 カレンダー情報要求

    リクエストボディに指定されたコミュニティ ID と日付をもとに、
    タグ情報を取得して JSON で返却するエンドポイント。

    Args:
        request (flask.Request):  
            JSON ボディに以下のキーを含む必要があります。  
            - community_id (str): コミュニティ ID  
            - date (date): 日付

    Returns:
        flask.Response: JSON レスポンス。返却される辞書の構造は以下のとおりです。  
            - data (List[Tag]): タグオブジェクトのリスト（成功時のみ）  
            - result (bool): 成功フラグ（True: 成功/False: 失敗）  
            - message (str): 処理結果の説明メッセージ  

        HTTP ステータスコード:  
            - 200: タグ取得成功  
            - 400: リクエスト不備（community_id または date 未指定、ボディが空）  
            - 500: サーバ内部エラー
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"result": False, "message": "リクエストボディが空です。"}), 400
    
    community_id = data.get("community_id")
    date = data.get("date")    
    
    if not community_id:
        return jsonify({"result": False, "message": "community_idが未指定です。"}), 400
    
    if not date:
        return jsonify({"result": False, "message": "dateが未指定です。"}), 400
    
    result = manager.request_calendar_data(community_id, date)
    if result["result"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@calendar_manager_bp.route('/tag/delete', methods=['DELETE'])
def manager_tag_delete():
    """
    C10 M3 タグ削除要求

    指定されたタグIDのタグを削除し、結果を JSON で返却するエンドポイント。

    Args:
        request (flask.Request):
            JSON ボディに以下のキーを含むこと。
            - tag_id (str): 削除対象のタグID

    Returns:
        flask.Response: JSON レスポンスとステータスコード
            - 200: {'result': True,  'message': 'タグを削除しました。'}
            - 400: {'result': False, 'message': 'リクエストボディが空です。' または 'tag_idが未指定です。'}
            - 404: {'result': False, 'message': 'タグが見つかりません。'}
            - 500: {'result': False, 'message': 'タグの削除に失敗しました。：<例外メッセージ>'}
    """
    data = request.get_json()
    if not data:
        return jsonify({"result": False, "message": "リクエストボディが空です。"}), 400

    tag_id = data.get("tag_id")

    if not tag_id:
        return jsonify({"result": False, "message": "tag_idが未指定です。"}), 400

    result = manager.tag_delete(tag_id)
    if result["result"]:
        return jsonify(result), 200
    else:
        status_code = 404 if "見つかりません" in result["message"] else 500
        return jsonify(result), status_code

@calendar_manager_bp.route('/tag/add', methods=['POST'])
def manager_tag_save():
    """
    C10 M4 タグ投稿データ保存要求

    リクエストボディに含まれるタグ情報をもとに、新しいタグをDBに保存し、
    結果をJSONで返却するエンドポイント。

    Args:
        request (flask.Request):
            JSON ボディに以下のキーを含む必要があります。
            - tag_id (str): タグID
            - tag_name (str): 表示名
            - tag_color (str): タグのカラーコード（例: 'FF0000'）
            - submitter_id (str): タグ登録者のユーザーID
            - community_id (str): コミュニティID
            - date (str): 日付（'YYYY-MM-DD'形式）

    Returns:
        flask.Response: JSONレスポンスとステータスコード
            - 200: {'result': True, 'message': "...", 'tag': {...}}
            - 400: {'result': False, 'message': "...が未指定です"} 又は {'result': False, 'message': "既に存在するタグです"}
            - 500: {'result': False, 'message': "タグの追加に失敗しました: <例外メッセージ>"}
    """
    data = request.get_json()
    if not data:
        return jsonify({"result": False, "message": "リクエストボディが空です。"}), 400

    tag_id = data.get("tag_id")
    tag_name = data.get("tag_name")
    tag_color = data.get("tag_color")
    submitter_id = data.get("submitter_id")
    community_id = data.get("community_id")
    date = data.get("date")

    if not tag_id:
        return jsonify({"result": False, "message": "tag_idが未指定です。"}), 400
    if not tag_name:
        return jsonify({"result": False, "message": "tag_nameが未指定です。"}), 400
    if not tag_color:
        return jsonify({"result": False, "message": "tag_colorが未指定です。"}), 400
    if not submitter_id:
        return jsonify({"result": False, "message": "submitter_idが未指定です。"}), 400
    if not community_id:
        return jsonify({"result": False, "message": "community_idが未指定です。"}), 400
    if not date:
        return jsonify({"result": False, "message": "dateが未指定です。"}), 400
    
    result = manager.tag_data_save(tag_id, tag_name, tag_color, submitter_id, community_id, date)
    if result["result"]:
        return jsonify(result), 200
    else:
        status_code = 400 if "既に存在" in result["message"] else 500
        return jsonify(result), status_code


