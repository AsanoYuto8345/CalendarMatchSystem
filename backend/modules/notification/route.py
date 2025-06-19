# C7通知処理部のM1通知送信主処理を担当するプログラム　担当: 浅野勇翔

from flask import Blueprint, request, jsonify
from .notification import Notification

notification_bp = Blueprint('notification', __name__, url_prefix='/api/notification')

@notification_bp.route('/notify', methods=['POST'])
def send_notify():
    """
    通知処理部のAPIエンドポイント。
    /api/notification/ にPOSTリクエストを受信した際に実行される。

    受信したユーザIDリストおよびメッセージ内容に基づき、
    LINE Messaging API を利用して該当ユーザにメッセージ通知を行う。

    入力バリデーション(E1)およびLINE API通信失敗(E2)に対して適切なHTTPステータスコードを返却する。

    Request JSON:
        {
            "user_ids": [str, ...],  # 通知対象ユーザのLINE ID (Uで始まる文字列)
            "message": str           # 通知メッセージ本文
        }

    Returns:
        flask.Response: JSON形式のレスポンスを返却
        - 200 OK: 通知送信成功
        - 400 Bad Request: ユーザID未指定・形式不正またはメッセージ未指定 (E1)
        - 502 Bad Gateway: LINE API通信失敗 (E2)
        - 500 Internal Server Error: 想定外のシステムエラー
    """
   
    data = request.json
    user_ids = data.get("user_ids", [])
    message = data.get("message", "")
    
    # E1: 入力エラーチェック
    if not user_ids or not all(isinstance(uid, str) and uid.startswith("U") for uid in user_ids):
        jsonify({"error": "ユーザIDが未指定または形式不正です"}), 400
    
    if not message:
        return jsonify({"error": "メッセージが未指定です"}), 400
    
    try:    
        ntf = Notification()
        send_result = ntf.send_match_message(user_ids, message)
        
        # メッセージ送信結果によって対応したjsonを返す
        if send_result:
            return jsonify({"msg": "送信完了", "result": True}), 200
        else:
            # E2 LINE API通信失敗
            return jsonify({"error": "LINE API通信失敗"}), 502
    except Exception as e:
        return jsonify({"error": "想定外エラー", "details": str(e)}), 500
            