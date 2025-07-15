import sqlite3
import os
import secrets  # SID生成用
import logging  # コーディング規約に沿ってログ出力を設定

# 担当者:関太生
# ロガー設定 (utils/logger.py があればそれを使用、なければ基本的な設定)
try:
    from utils.logger import setup_logger
    user_management_logger = setup_logger(__name__)
except ImportError:
    logging.basicConfig(level=logging.INFO)
    user_management_logger = logging.getLogger(__name__)

# DBファイルのパスは環境変数または設定ファイルで管理することを推奨
DATABASE_NAME = os.getenv('DATABASE_NAME', 'instance/messages.db')


class UserDataManagement:
    """
    C8 ユーザ情報管理部のM1 ユーザ情報管理主処理クラスに対応。
    C2ユーザ認証処理部やC3ユーザ情報処理部よりユーザデータを受け取り、
    ユーザデータを各処理メソッドで処理し、各コンポーネントに返却する。
    """

    def __init__(self):
        self.conn = None
        self.cursor = None
        self._connect_db()
        self._create_tables_if_not_exists()

    def _connect_db(self):
        """データベースに接続する内部メソッド"""
        try:
            os.makedirs(os.path.dirname(DATABASE_NAME), exist_ok=True)
            self.conn = sqlite3.connect(DATABASE_NAME)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            user_management_logger.info(f"Connected to database: {DATABASE_NAME}")
        except sqlite3.Error as e:
            user_management_logger.error(f"Database connection error: {e}")
            raise

    def _close_db(self):
        """データベース接続を閉じる内部メソッド"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            user_management_logger.info("Database connection closed.")

    def _create_tables_if_not_exists(self):
        """
        F1 ユーザ情報とF2 ユーザ認証情報のテーブルを作成
        """
        try:
            self._connect_db()
            self.cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    user_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    profile_image TEXT
                )
                '''
            )
            self.cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS user_auth (
                    user_id TEXT NOT NULL,
                    sid TEXT PRIMARY KEY,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
                '''
            )
            self.conn.commit()
            user_management_logger.info("Tables 'users' and 'user_auth' checked/created successfully.")
        except sqlite3.Error as e:
            user_management_logger.error(f"Error creating tables: {e}")
            raise
        finally:
            self._close_db()

    def user_data_search(self, user_id):
        """
        M2 ユーザ情報検索処理に対応
        user_id をもとにユーザデータを検索し、返却
        """
        user_management_logger.info(f"Searching user data for user_id: {user_id}")
        try:
            self._connect_db()
            self.cursor.execute(
                "SELECT user_id, user_name, email, password, profile_image FROM users WHERE user_id = ?",
                (user_id,)
            )
            user_data = self.cursor.fetchone()
            if user_data:
                user_dict = {
                    "id": user_data["user_id"],
                    "name": user_data["user_name"],
                    "email": user_data["email"],
                    "password": user_data["password"],
                    "icon": user_data["profile_image"]
                }
                return True, user_dict
            else:
                user_management_logger.warning(f"User data not found for ID: {user_id}. (E2)")
                return False, {}
        except sqlite3.Error as e:
            user_management_logger.error(f"Database error during user data search: {e}")
            raise
        finally:
            self._close_db()

    def make_sid(self, user_id: str):
        """
        M3 SID作成処理に対応
        ユーザIDを受け取り、F2 ユーザ認証情報にSIDを作成する。
        """
        user_management_logger.info(f"Attempting to create SID for user_id: {user_id}")
        sid = secrets.token_urlsafe(16)
        try:
            self._connect_db()
            self.cursor.execute(
                "INSERT INTO user_auth (user_id, sid) VALUES (?, ?)",
                (user_id, sid)
            )
            self.conn.commit()
            return sid
        except sqlite3.IntegrityError as e:
            user_management_logger.warning(f"SID creation failed for user_id {user_id}: {e}")
            return None
        except sqlite3.Error as e:
            user_management_logger.error(f"Database error during SID creation for user_id {user_id}: {e}")
            raise
        finally:
            self._close_db()

    def delete_sid(self, sid):
        """
        M4 SID破棄処理に対応
        """
        user_management_logger.info(f"Attempting to delete SID: {sid}")
        try:
            self._connect_db()
            self.cursor.execute("DELETE FROM user_auth WHERE sid = ?", (sid,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            user_management_logger.error(f"Database error during SID deletion for {sid}: {e}")
            raise
        finally:
            self._close_db()

    def register_user_data(self, user_id, hashed_pw, name, email, icon):
        """
        M5 ユーザ情報登録処理に対応
        """
        user_management_logger.info(f"Registering user data for user_id: {user_id}")
        try:
            self._connect_db()
            self.cursor.execute(
                "INSERT INTO users (user_id, user_name, email, password, profile_image) VALUES (?, ?, ?, ?, ?)",
                (user_id, name, email, hashed_pw, icon)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            user_management_logger.warning(f"User {user_id} or email {email} already exists: {e} (E3)")
            return False
        except sqlite3.Error as e:
            user_management_logger.error(f"Database error during user registration: {e}")
            raise
        finally:
            self._close_db()

    def update_user_data(self, user_id, hashed_pw=None, name=None, email=None, icon=None):
        """
        M6 ユーザ情報更新処理に対応
        """
        user_management_logger.info(f"Updating user data for user_id: {user_id}")
        update_fields = []
        params = []

        if hashed_pw:
            update_fields.append("password = ?")
            params.append(hashed_pw)
        if name:
            update_fields.append("user_name = ?")
            params.append(name)
        if email:
            update_fields.append("email = ?")
            params.append(email)
        if icon:
            update_fields.append("profile_image = ?")
            params.append(icon)

        if not update_fields:
            user_management_logger.warning(f"No fields to update for user {user_id}.")
            return False

        params.append(user_id)
        set_clause = ", ".join(update_fields)

        try:
            self._connect_db()
            self.cursor.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", tuple(params))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            user_management_logger.warning(f"Integrity error during user update for {user_id}: {e}")
            return False
        except sqlite3.Error as e:
            user_management_logger.error(f"Database error during user update for {user_id}: {e}")
            raise
        finally:
            self._close_db()

    def find_login_user(self, email: str) -> tuple[bool, dict]:
        """
        M7 ログイン用ユーザ検索処理に対応
        メールアドレスをもとに users テーブルからユーザ情報を取得する。
        Returns:
            tuple[bool, dict]
        """
        user_management_logger.info(f"Searching login user for email: {email}")
        try:
            self._connect_db()
            self.cursor.execute(
                "SELECT user_id, user_name, email, password, profile_image FROM users WHERE email = ?",
                (email,)
            )
            row = self.cursor.fetchone()
            if row:
                user = {
                    "id": row["user_id"],
                    "name": row["user_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "icon": row["profile_image"]
                }
                return True, user
            else:
                user_management_logger.warning(f"Login user not found for email: {email}")
                return False, {}
        except sqlite3.Error as e:
            user_management_logger.error(f"Database error during login user search for {email}: {e}")
            raise
        finally:
            self._close_db()

    def validate_sid(self, user_id: str, sid: str) -> bool:
        """
        M8 SID検証処理に対応
        user_authテーブルに指定されたuser_idとsidの組み合わせが存在するかをチェックする。
        Returns:
            bool: 存在する場合はTrue、存在しない場合はFalse
        """
        user_management_logger.info(f"Validating SID for user_id: {user_id}, sid: {sid}")
        try:
            self._connect_db()
            self.cursor.execute(
                "SELECT 1 FROM user_auth WHERE user_id = ? AND sid = ?",
                (user_id, sid)
            )
            result = self.cursor.fetchone()
            return result is not None
        except sqlite3.Error as e:
            user_management_logger.error(f"Database error during SID validation for user_id {user_id}: {e}")
            raise
        finally:
            self._close_db()
