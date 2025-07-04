# routes/routes.py
# C1 UI処理部とC2 ユーザ認証処理部の間を繋ぐAPIルーティング
# 担当: 石田めぐみ (UserAuthを担当)

from flask import Blueprint, request, jsonify, current_app
import os
import logging

# UserAuthとPasswordHasherをインポート
# Assuming user_auth.py is in modules/Loginout/
from modules.Loginout.user_auth import UserAuth, SHA256PasswordHasher

# ロギング設定
logger = logging.getLogger(__name__)

# Blueprintの定義
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# UserAuthのインスタンスはアプリケーション起動時に初期化されることを想定
user_auth_instance: UserAuth = None

def init_app(app_instance):
    """
    Flaskアプリケーションインスタンスの初期化時にUserAuthをセットアップします。
    """
    global user_auth_instance
    password_hasher = SHA256PasswordHasher()
    user_auth_instance = UserAuth(password_hasher=password_hasher)
    logger.info("UserAuth instance initialized in auth_routes.py")


@auth_bp.route('/login', methods=['POST'])
def login_route():
    """
    M2 ログイン処理のAPIエンドポイント。
    メールアドレスとパスワードでユーザー認証を行い、成功時にセッションIDを返す。
    """
    if not request.is_json:
        logger.warning("login_route: Request must be JSON.")
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json
    email = data.get('email')
    password = data.get('pw')

    # E1: 入力エラーチェック (メールアドレス、パスワードの未指定)
    if not email or not isinstance(email, str):
        logger.warning("login_route: Email is missing or invalid type.")
        return jsonify({"error": "メールアドレスが未指定または形式不正です"}), 400
    if not password or not isinstance(password, str):
        logger.warning("login_route: Password is missing or invalid type.")
        return jsonify({"error": "パスワードが未指定です"}), 400

    # UserAuthインスタンスが存在することを確認
    if user_auth_instance is None:
        logger.error("login_route: UserAuth instance not initialized.")
        return jsonify({"error": "サーバー内部エラー"}), 500

    # ここでsignin_userにemailとpasswordを渡しているため、修正は不要です。
    success, sid = user_auth_instance.signin_user(email, password)

    if success:
        logger.info(f"login_route: Login successful for email: {email}")
        return jsonify({"message": "Login successful", "sid": sid}), 200
    else:
        # UserAuthのsignin_userは、認証失敗時（ユーザー不在、パスワード不一致など）にFalseを返す
        logger.warning(f"login_route: Login failed for email: {email}")
        return jsonify({"error": "メールアドレスまたはパスワードが不正です"}), 401 # 401 Unauthorized


@auth_bp.route('/logout', methods=['DELETE']) # 設計書とuser_auth.pyの整合性からDELETEに統一
def logout_route():
    """
    M3 ログアウト処理のAPIエンドポイント。
    セッションIDを受け取り、C8にセッション削除を依頼する。
    """
    # DELETEリクエストの場合、JSONボディまたはURLパラメータからsidを取得することを考慮
    sid = None
    if request.is_json:
        data = request.json
        sid = data.get('sid')
    else: # JSONボディでない場合（例: GETリクエストのようにURLパラメータで渡すDELETEリクエスト）
        sid = request.args.get('sid') # クエリパラメータから取得

    # E1: 入力エラーチェック (SIDの未指定)
    if not sid or not isinstance(sid, str):
        logger.warning(f"logout_route: Session ID (sid) is missing or invalid type: {sid}")
        return jsonify({"error": "セッションIDが未指定または形式不正です"}), 400
    
    # UserAuthインスタンスが存在することを確認
    if user_auth_instance is None:
        logger.error("logout_route: UserAuth instance not initialized.")
        return jsonify({"error": "サーバー内部エラー"}), 500

    success = user_auth_instance.signout_user(sid)

    if success:
        logger.info(f"logout_route: Logout successful for SID: {sid}")
        return jsonify({"message": "Logout successful"}), 200
    else:
        # user_auth_instance.signout_userがFalseを返すのはC8との通信失敗など
        logger.error(f"logout_route: Logout failed for SID: {sid} due to internal error or C8 issue.")
        return jsonify({"error": "ログアウト処理中にエラーが発生しました"}), 500 # 500 Internal Server Error