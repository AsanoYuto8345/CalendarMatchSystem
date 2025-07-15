# c3_user_routes.py
# C3 ユーザ情報処理部のAPIエンドポイントを定義
# 作成者:関太生

from flask import Blueprint, request, jsonify
# C3のビジネスロジックをインポート
from .user_data_process import UserDataProcess

# Blueprintの定義。URLプレフィックスは /api/user とする
user_data_bp = Blueprint('user_data', __name__, url_prefix='/api/user')


## User Registration

@user_data_bp.route('/register', methods=['POST'])
def register_user():
    """
    ユーザ登録のAPIエンドポイント。
    /api/user/register にPOSTリクエストを受信した際に実行される。

    Request Data (multipart/form-data):
        email (str): ユーザのメールアドレス
        password (str): ユーザのパスワード
        name (str): ユーザの表示名
        icon_file (File): アイコン画像ファイル (任意)

    Returns:
        flask.Response: JSON形式のレスポンスを返却
        - 200 OK: ユーザ登録成功
        - 400 Bad Request: 入力データ形式不正または不足 (E1)
        - 409 Conflict: 登録しようとしたユーザIDがすでに存在する場合 (E3)
        - 500 Internal Server Error: その他のシステムエラー
    """
    # multipart/form-data からデータを取得
    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    icon_file = request.files.get("icon_file") # request.files からファイルを取得

    user_process = UserDataProcess()
    result = user_process.data_regist(email, password, name, icon_file) # icon_file を渡す

    if result["result"]:
        return jsonify({"message": "ユーザ登録成功", "user_id": result["user_id"], "icon_path": result.get("icon_name")}), 200
    else:
        # E1, E3のエラーハンドリング
        return jsonify({"error": result.get("error", "ユーザ登録失敗")}), \
               result.get("status", 500)

## User Data Editing

@user_data_bp.route('/edit', methods=['PUT'])
def edit_user_data():
    """
    ユーザ情報編集のAPIエンドポイント。
    /api/user/edit にPUTリクエストを受信した際に実行される。

    Request Data (multipart/form-data):
        user_id (str): 編集対象のユーザID
        password (str, optional): 新しいパスワード
        name (str, optional): 新しい表示名
        icon_file (File, optional): 新しいアイコン画像ファイル
        email (str, optional): 新しいメールアドレス
        # アイコンを削除する場合の特別なキー (例: "delete_icon": "true") は今回は考慮しないが、必要であれば追加
    Returns:
        flask.Response: JSON形式のレスポンスを返却
        - 200 OK: ユーザ情報編集成功
        - 400 Bad Request: 入力データ形式不正または不足 (E1)
        - 404 Not Found: 編集対象のユーザが存在しない場合 (E2)
        - 500 Internal Server Error: その他のシステムエラー
    """
    # PUTリクエストでmultipart/form-dataを扱う場合、request.formとrequest.filesを使用
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    name = request.form.get("name")
    icon_file = request.files.get("icon_file") # request.files からファイルを取得
    email = request.form.get("email")

    user_process = UserDataProcess()
    result = user_process.data_edit(user_id, password, name, icon_file, email) # icon_file を渡す

    if result["result"]:
        return jsonify({"message": "ユーザ情報編集成功", "icon_path": result.get("icon_name")}), 200
    else:
        # E1, E2のエラーハンドリング
        return jsonify({"error": result.get("error", "ユーザ情報編集失敗")}), \
               result.get("status", 500)


## User Data Retrieval

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
