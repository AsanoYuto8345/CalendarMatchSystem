# modules/users/route.py
# C8 ユーザ情報管理部のAPIエンドポイントを定義
# 担当者:関太生

from flask import Blueprint, request, jsonify
from .user_data_management import UserDataManagement
import logging

# ロガー設定 (utils/logger.py があればそれを使用、なければ基本的な設定)
try:
    from utils.logger import setup_logger
    user_logger = setup_logger(__name__)
except ImportError:
    logging.basicConfig(level=logging.INFO)
    user_logger = logging.getLogger(__name__)

# Blueprintの定義。URLプレフィックスは /api となっている
user_bp = Blueprint('users', __name__, url_prefix='/api')

@user_bp.route('/users/search', methods=['GET'])
def search_user_data():
    """
    M2 ユーザ情報検索処理に対応
    ユーザIDをもとにユーザデータを検索し、返す。
    """
    user_id = request.args.get('id')
    if not user_id:
        user_logger.warning("User ID is missing for search request.")
        return jsonify({"message": "User ID is required"}), 400
    try:
        um = UserDataManagement()
        found, user = um.user_data_search(user_id)
        if found:
            user_logger.info(f"User data found for ID: {user_id}")
            return jsonify({
                "id": user.get('id'),
                "email": user.get('email'),
                "name": user.get('name'),
                "icon": user.get('icon')
            }), 200
        else:
            user_logger.info(f"User data not found for ID: {user_id}")
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        user_logger.error(f"Error searching user data for ID {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500

@user_bp.route('/sid/create', methods=['POST'])
def create_sid():
    """
    M3 SID作成処理に対応
    ユーザIDを受け取り、F2 ユーザ認証情報にSIDを作成する。
    """
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        user_logger.warning("user_id is missing for SID creation request.")
        return jsonify({"message": "user_id is required"}), 400
    try:
        um = UserDataManagement()
        sid = um.make_sid(user_id)
        if sid:
            user_logger.info(f"SID created for user_id {user_id}.")
            return jsonify({"sid": sid}), 200
        else:
            user_logger.warning(f"Failed to create SID for user_id {user_id}.")
            return jsonify({"message": "Failed to create SID"}), 500
    except Exception as e:
        user_logger.error(f"Error creating SID for user_id {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500

@user_bp.route('/sid/delete', methods=['DELETE'])
def delete_sid():
    """
    M4 SID破棄処理に対応
    SIDを受け取り、F2 ユーザ認証情報から破棄する。
    """
    data = request.json
    sid = data.get('sid')
    if not sid:
        user_logger.warning("SID is missing for deletion request.")
        return jsonify({"message": "SID is required"}), 400
    try:
        um = UserDataManagement()
        result = um.delete_sid(sid)
        if result:
            user_logger.info(f"SID {sid} deleted successfully.")
            return jsonify({"message": "SID deleted successfully"}), 200
        else:
            user_logger.warning(f"SID {sid} not found or deletion failed.")
            return jsonify({"message": "SID not found or deletion failed"}), 404
    except Exception as e:
        user_logger.error(f"Error deleting SID {sid}: {e}")
        return jsonify({"message": "Internal server error"}), 500

@user_bp.route('/users/register', methods=['POST'])
def register_user_data():
    """
    M5 ユーザ情報登録処理に対応
    新しいユーザデータをF1 ユーザ情報に登録する。
    """
    data = request.json
    user_id = data.get('id')
    hashed_pw = data.get('hashed_pw')
    name = data.get('name')
    icon = data.get('icon')
    email = data.get('email')
    if not all([user_id, hashed_pw, name, email]):
        user_logger.warning("Missing required fields for user registration.")
        return jsonify({"message": "Missing required fields"}), 400
    try:
        um = UserDataManagement()
        result = um.register_user_data(user_id, hashed_pw, name, email, icon)
        if result:
            user_logger.info(f"User {user_id} registered successfully.")
            return jsonify({"message": "User registered successfully"}), 201
        else:
            user_logger.warning(f"User {user_id} already exists or registration failed.")
            return jsonify({"message": "User already exists or registration failed"}), 409
    except Exception as e:
        user_logger.error(f"Error registering user {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500

@user_bp.route('/users/update', methods=['PUT'])
def update_user_data():
    """
    M6 ユーザ情報更新処理に対応
    既存のユーザデータを更新する。
    """
    data = request.json
    user_id = data.get('id')
    hashed_pw = data.get('hashed_pw')
    name = data.get('name')
    icon = data.get('icon')
    email = data.get('email')
    if not user_id:
        user_logger.warning("User ID is missing for update request.")
        return jsonify({"message": "User ID is required"}), 400
    try:
        um = UserDataManagement()
        result = um.update_user_data(user_id, hashed_pw, name, email, icon)
        if result:
            user_logger.info(f"User {user_id} updated successfully.")
            return jsonify({"message": "User updated successfully"}), 200
        else:
            user_logger.warning(f"User {user_id} not found or update failed.")
            return jsonify({"message": "User not found or update failed"}), 404
    except Exception as e:
        user_logger.error(f"Error updating user {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500

@user_bp.route('/users/login', methods=['GET'])
def find_login_user_route():
    """
    M7 ログイン用ユーザ検索エンドポイント。
    クエリパラメータ email を受け取り、該当ユーザを返す。
    """
    email = request.args.get('email')
    if not email or not isinstance(email, str):
        user_logger.warning("find_login_user_route: email is missing or invalid")
        return jsonify({"error": "email パラメータが必要です"}), 400
    try:
        um = UserDataManagement()
        found, user = um.find_login_user(email)
        if found:
            user_logger.info(f"find_login_user_route: User found for email {email}")
            return jsonify({"user_data": user}), 200
        else:
            user_logger.warning(f"find_login_user_route: User not found for email {email}")
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        user_logger.error(f"find_login_user_route: Error while searching user {email}: {e}")
        return jsonify({"error": "Internal server error"}), 500

@user_bp.route('/sid/validate', methods=['POST'])
def validate_sid_route():
    """
    M8 SID検証処理エンドポイント。
    JSONで user_id と sid を受け取り、一致するレコードの有無を返す。
    """
    data = request.json
    user_id = data.get('user_id')
    sid     = data.get('sid')
    if not user_id or not sid:
        user_logger.warning("validate_sid_route: user_id or sid is missing")
        return jsonify({"error": "user_id and sid are required"}), 400
    try:
        um = UserDataManagement()
        valid = um.validate_sid(user_id, sid)
        return jsonify({"valid": valid}), 200
    except Exception as e:
        user_logger.error(f"validate_sid_route: Error validating SID for user_id {user_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500
