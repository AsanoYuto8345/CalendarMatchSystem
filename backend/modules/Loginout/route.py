# modules/users/route.py
# ユーザ認証関連のルーティング定義
# 担当: 石田めぐみ

from flask import Blueprint, request, jsonify, make_response
from modules.Loginout.user_auth import UserAuth, InMemorySessionStore, SHA256PasswordHasher
from modules.users.user_data_management import UserDataManagement # C8 ユーザー情報管理部をインポート

# Blueprintの初期化
user_bp = Blueprint("users", __name__, url_prefix="/api/auth")

# UserAuthの初期化（実際にはDIコンテナなどから注入する）
# ここでは簡易のために直接インスタンス化
session_store = InMemorySessionStore()
password_hasher = SHA256PasswordHasher()
user_data_manager = UserDataManagement() # C8 ユーザー情報管理部のインスタンス
user_auth = UserAuth(session_store, password_hasher, user_data_manager)

@user_bp.route("/auth_main", methods=["GET"])
def auth_main():
    """
    M1 認証主処理のエンドポイント。
    設計書に従い、URLを受け取り、ステータスとセッションIDを返す。
    （M1の「認証主処理」は、通常、セッションの有効性確認やトークン検証に用いられるが、
    設計書ではURL入力とダミーセッションID発行とあるため、それに準拠）
    """
    # 設計書に従い、URLをクエリパラメータとして受け取ることを想定
    url = request.args.get("url")

    if not url:
        return make_response(
            jsonify({"message": "URL parameter is required"}),
            400
        )

    status, sid = user_auth.handle_auth(url)

    if status == 200:
        return make_response(
            jsonify({"message": "Auth main process successful", "session_id": sid}),
            status
        )
    else:
        # E1: URL形式不正
        return make_response(
            jsonify({"message": "URL format is invalid", "status": status}),
            status
        )

@user_bp.route("/login", methods=["POST"])
def login():
    """
    M2 ログイン処理のエンドポイント。
    C1 UI処理部からメールアドレスとパスワードを受け取り、
    UserAuth の signin_user 関数に処理を依頼する。
    成功すれば処理の成否とセッションIDを返す。
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return make_response(
            jsonify({"result": False, "message": "Email and password are required"}),
            400
        )

    result, sid = user_auth.signin_user(email, password)

    if result:
        response = make_response(
            jsonify({"result": True, "message": "Login successful", "session_id": sid}),
            200
        )
        # セッションIDをHTTP Only Cookieに設定することも検討する
        # response.set_cookie('session_id', sid, httponly=True, secure=True)
        return response
    else:
        # 設計書のE2エラー（ユーザーが見つからない、またはパスワード不一致）
        return make_response(
            jsonify({"result": False, "message": "Login failed: Invalid credentials or user not found."}),
            401 # Unauthorized
        )


@user_bp.route("/logout", methods=["POST"])
def logout():
    """
    M3 ログアウト処理のエンドポイント。
    C1 UI処理部からセッションIDを受け取り、
    UserAuth の signout_user 関数に処理を依頼する。
    処理の成否を返す。
    """
    # 設計書では M1 からセッションIDを受け取るとあるが、
    # 実際のフローでは C1 UI処理部 (例: ヘッダーまたはCookie) から受け取る
    session_id = request.headers.get("X-Session-ID")
    # または session_id = request.cookies.get('session_id')

    if not session_id:
        return make_response(
            jsonify({"result": False, "message": "Session ID is required"}),
            400
        )

    result = user_auth.signout_user(session_id)

    if result:
        response = make_response(jsonify({"result": True, "message": "Logout successful"}), 200)
        # CookieからセッションIDを削除する場合
        # response.set_cookie('session_id', '', expires=0, httponly=True, secure=True)
        return response
    else:
        # セッションIDが無効な場合など
        return make_response(
            jsonify({"result": False, "message": "Logout failed: Session ID is invalid or not found."}),
            400
        )