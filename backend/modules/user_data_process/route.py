# C3 ユーザ情報処理部のAPIエンドポイントを定義
# 作成者: [担当者の名前]

from flask import Blueprint, request, jsonify
from user_data_process import UserDataProcess

user_data_bp = Blueprint('user_data', __name__, url_prefix='/api/user')

@user_data_bp.route('/register', methods=['POST'])
def register_user():
    """
    ユーザ登録のAPIエンドポイント。
    /api/user/register にPOSTリクエストを受信した際に実行される。

    Request JSON:
        {
            "email": "str",      # ユーザのメールアドレス
            "password": "str",   # ユーザのパスワード
            "name": "str",       # ユーザの表示名
            "icon_name": "str"   # アイコンのファイル名 (任意)
        }
    Returns:
        flask.Response: JSON形式のレスポンスを返却
        - 200 OK: ユーザ登録成功
        - 400 Bad Request: 入力データ形式不正または不足 (E1)
        - 409 Conflict: 登録しようとしたユーザIDがすでに存在する場合 (E3)
        - 500 Internal Server Error: その他のシステムエラー
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    icon_name = data.get("icon_name", "default_icon.png")

    user_process = UserDataProcess()
    result = user_process.data_regist(email, password, name, icon_name)

    if result["result"]:
        return jsonify({"message": "ユーザ登録成功", "user_id": result["user_id"]}), 200
    else:
        # E1, E3のエラーハンドリング
        return jsonify({"error": result.get("error", "ユーザ登録失敗")}), \
               result.get("status", 500)


@user_data_bp.route('/edit', methods=['PUT'])
def edit_user_data():
    """
    ユーザ情報編集のAPIエンドポイント。
    /api/user/edit にPUTリクエストを受信した際に実行される。

    Request JSON:
        {
            "user_id": "str",        # 編集対象のユーザID
            "password": "str",       # 新しいパスワード (任意)
            "name": "str",           # 新しい表示名 (任意)
            "icon_name": "str"       # 新しいアイコンのファイル名 (任意)
        }
    Returns:
        flask.Response: JSON形式のレスポンスを返却
        - 200 OK: ユーザ情報編集成功
        - 400 Bad Request: 入力データ形式不正または不足 (E1)
        - 404 Not Found: 編集対象のユーザが存在しない場合 (E2)
        - 500 Internal Server Error: その他のシステムエラー
    """
    data = request.json
    user_id = data.get("user_id")
    password = data.get("password")
    name = data.get("name")
    icon_name = data.get("icon_name")

    user_process = UserDataProcess()
    result = user_process.data_edit(user_id, password, name, icon_name)

    if result["result"]:
        return jsonify({"message": "ユーザ情報編集成功"}), 200
    else:
        # E1, E2のエラーハンドリング
        return jsonify({"error": result.get("error", "ユーザ情報編集失敗")}), \
               result.get("status", 500)


@user_data_bp.route('/get/<string:user_id>', methods=['GET'])
def get_user_data(user_id: str):
    """
    ユーザ情報取得のAPIエンドポイント。
    /api/user/get/<user_id> にGETリクエストを受信した際に実行される。

    Args:
        user_id (str): 取得対象のユーザID

    Returns:
        flask.Response: JSON形式のレスポンスを返却
        - 200 OK: ユーザ情報取得成功
        - 400 Bad Request: ユーザIDが指定されていない場合 (E1)
        - 404 Not Found: 該当するユーザデータがない場合 (E2)
        - 500 Internal Server Error: その他のシステムエラー
    """
    user_process = UserDataProcess()
    result = user_process.data_get(user_id)

    if result["result"]:
        return jsonify({"message": "ユーザ情報取得成功", "user_data": result["user_data"]}), 200
    else:
        # E1, E2のエラーハンドリング
        return jsonify({"error": result.get("error", "ユーザ情報取得失敗")}), \
               result.get("status", 500)
