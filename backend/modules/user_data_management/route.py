# modules/users/route.py
# C8 ユーザ情報管理部のAPIエンドポイントを定義
# 作成者: [担当者の名前]

from flask import Blueprint, request, jsonify
from modules.users.user_data_management import UserDataManagement
import logging # コーディング規約に沿ってログ出力を設定 

# ロガー設定 (utils/logger.py があればそれを使用、なければ基本的な設定) 
try:
    from utils.logger import setup_logger
    user_logger = setup_logger(__name__)
except ImportError:
    logging.basicConfig(level=logging.INFO)
    user_logger = logging.getLogger(__name__)

# Blueprintの定義。URLプレフィックスは /api となっていることに注意
user_bp = Blueprint('users', __name__, url_prefix='/api')

@user_bp.route('/users/search', methods=['GET'])
def search_user_data():
    """
    M2 ユーザ情報検索処理に対応
    ユーザIDをもとにユーザデータを検索し、返す。 
    """
    user_id = request.args.get('id') # クエリパラメータからユーザIDを取得

    if not user_id:
        user_logger.warning("User ID is missing for search request.")
        return jsonify({"message": "User ID is required"}), 400 # E1: 不正なデータ形式 

    try:
        user_manager = UserDataManagement()
        # ユーザ情報検索処理の呼び出し 
        result, user_data = user_manager.user_data_search(user_id)

        if result:
            user_logger.info(f"User data found for ID: {user_id}")
            # パスワードはセキュリティ上返さない
            return jsonify({
                "id": user_data.get('id'),
                "email": user_data.get('email'),
                "name": user_data.get('name'),
                "icon": user_data.get('icon')
            }), 200
        else:
            user_logger.info(f"User data not found for ID: {user_id}")
            return jsonify({"message": "User not found"}), 404 # E2: 該当データなし 
    except Exception as e:
        user_logger.error(f"Error searching user data for ID {user_id}: {e}")
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
    email = data.get('email') # 外部設計書 F1 ユーザ情報より追加 

    # 入力値のバリデーション 
    if not all([user_id, hashed_pw, name, email]): # emailも必須項目として追加
        user_logger.warning("Missing required fields for user registration.")
        return jsonify({"message": "Missing required fields"}), 400 # E1: 不正なデータ形式 

    try:
        user_manager = UserDataManagement()
        # ユーザ情報登録処理の呼び出し 
        result = user_manager.register_user_data(user_id, hashed_pw, name, email, icon)

        if result:
            user_logger.info(f"User {user_id} registered successfully.")
            return jsonify({"message": "User registered successfully"}), 201
        else:
            user_logger.warning(f"User {user_id} already exists or registration failed.")
            # 内部設計書 E3: 登録済みデータあり  に基づき409を返す
            return jsonify({"message": "User already exists or registration failed"}), 409
    except Exception as e:
        user_logger.error(f"Error registering user {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500

@user_bp.route('/users/update', methods=['PUT'])
def update_user_data():
    """
    M6 ユーザ情報更新処理に対応
    既存のユーザデータをF1 ユーザ情報で更新する。 
    """
    data = request.json
    user_id = data.get('id')
    hashed_pw = data.get('hashed_pw')
    name = data.get('name')
    icon = data.get('icon')
    email = data.get('email') # 外部設計書 F1 ユーザ情報より追加 

    if not user_id:
        user_logger.warning("User ID is missing for update request.")
        return jsonify({"message": "User ID is required"}), 400 # E1: 不正なデータ形式 

    try:
        user_manager = UserDataManagement()
        # ユーザ情報更新処理の呼び出し 
        result = user_manager.update_user_data(user_id, hashed_pw, name, email, icon) # emailを追加

        if result:
            user_logger.info(f"User {user_id} updated successfully.")
            return jsonify({"message": "User updated successfully"}), 200
        else:
            user_logger.warning(f"User {user_id} not found or update failed.")
            return jsonify({"message": "User not found or update failed"}), 404 # E2: 該当データなし 
    except Exception as e:
        user_logger.error(f"Error updating user {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500

@user_bp.route('/sid/create', methods=['POST'])
def create_sid():
    """
    M3 SID作成処理に対応
    ユーザを認証するためのSIDをF2 ユーザ認証情報に作成する。 
    """
    data = request.json
    user_id = data.get('id')

    if not user_id:
        user_logger.warning("User ID is missing for SID creation request.")
        return jsonify({"message": "User ID is required"}), 400

    try:
        user_manager = UserDataManagement()
        # SID作成処理の呼び出し 
        sid = user_manager.make_sid(user_id)

        if sid:
            user_logger.info(f"SID created for user {user_id}.")
            return jsonify({"sid": sid}), 200
        else:
            user_logger.warning(f"Failed to create SID for user {user_id}.")
            return jsonify({"message": "Failed to create SID"}), 500
    except Exception as e:
        user_logger.error(f"Error creating SID for user {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500

@user_bp.route('/sid/delete', methods=['DELETE'])
def delete_sid():
    """
    M4 SID破棄処理に対応
    入力されたSIDをF2 ユーザ認証情報から破棄する。 
    """
    data = request.json
    sid = data.get('sid')

    if not sid:
        user_logger.warning("SID is missing for deletion request.")
        return jsonify({"message": "SID is required"}), 400

    try:
        user_manager = UserDataManagement()
        # SID破棄処理の呼び出し 
        result = user_manager.delete_sid(sid)

        if result:
            user_logger.info(f"SID {sid} deleted successfully.")
            return jsonify({"message": "SID deleted successfully"}), 200
        else:
            user_logger.warning(f"SID {sid} not found or deletion failed.")
            return jsonify({"message": "SID not found or deletion failed"}), 404
    except Exception as e:
        user_logger.error(f"Error deleting SID {sid}: {e}")
        return jsonify({"message": "Internal server error"}), 500
