# modules/users/user_data_management.py
# C8 ユーザ情報管理部のM1 ユーザ情報管理主処理クラスに対応
# 作成者: [担当者の名前]

import sqlite3
import os
import secrets # SID生成用 
import logging # コーディング規約に沿ってログ出力を設定 

# ロガー設定 (utils/logger.py があればそれを使用、なければ基本的な設定) 
try:
    from utils.logger import setup_logger
    user_management_logger = setup_logger(__name__)
except ImportError:
    logging.basicConfig(level=logging.INFO)
    user_management_logger = logging.getLogger(__name__)

# DBファイルのパスは環境変数または設定ファイルで管理することを推奨 
DATABASE_NAME = os.getenv('DATABASE_NAME', 'data/calendar.db') # 外部設計書 F1,F2,F3,F4物理的位置参照 

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
        self._create_tables_if_not_exists() # テーブルが存在しない場合に作成

    def _connect_db(self):
        """データベースに接続する内部メソッド"""
        try:
            # dataフォルダが存在しない場合は作成 
            os.makedirs(os.path.dirname(DATABASE_NAME), exist_ok=True)
            self.conn = sqlite3.connect(DATABASE_NAME)
            self.conn.row_factory = sqlite3.Row # row_factoryを設定して辞書形式で結果を取得
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
            self._connect_db() # テーブル作成前にDB接続を再確認
            # F1 ユーザ情報テーブル 
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    user_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    profile_image TEXT
                )
            ''')
            # F2 ユーザ認証情報テーブル 
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_auth (
                    user_id TEXT NOT NULL,
                    sid TEXT PRIMARY KEY,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
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
        入力されたユーザIDをもとにF1ユーザ情報からユーザデータを検索し、返す。 
        Args:
            user_id (str): 検索対象のユーザID
        Returns:
            tuple[bool, dict]: 処理の成否とユーザデータ辞書。 
                               該当データなしの場合、Falseと空の辞書を返す。
        """
        user_management_logger.info(f"Searching user data for user_id: {user_id}")
        try:
            self._connect_db() # 検索前にDB接続を再確認
            self.cursor.execute("SELECT user_id, user_name, email, password, profile_image FROM users WHERE user_id = ?", (user_id,))
            user_data = self.cursor.fetchone()
            if user_data:
                # row_factoryを設定しているため、直接辞書としてアクセス可能
                user_dict = {
                    "id": user_data["user_id"],
                    "name": user_data["user_name"],
                    "email": user_data["email"],
                    "password": user_data["password"],
                    "icon": user_data["profile_image"]
                }
                return True, user_dict
            else:
                user_management_logger.warning(f"User data not found for ID: {user_id}. (E2)") # E2: 該当データなし 
                return False, {}
        except sqlite3.Error as e:
            user_management_logger.error(f"Database error during user data search: {e}")
            raise
        finally:
            self._close_db()

    def register_user_data(self, user_id, hashed_pw, name, email, icon):
        """
        M5 ユーザ情報登録処理に対応 
        新しいユーザデータをF1 ユーザ情報に登録する。 
        Args:
            user_id (str): 登録するユーザID
            hashed_pw (str): ハッシュ化されたパスワード
            name (str): 表示名
            email (str): メールアドレス 
            icon (str): アイコンのファイル名
        Returns:
            bool: 処理の成否 (True: 成功, False: 失敗 - 例: 重複データ) 
        """
        user_management_logger.info(f"Registering user data for user_id: {user_id}")
        try:
            self._connect_db() # 登録前にDB接続を再確認
            self.cursor.execute("INSERT INTO users (user_id, user_name, email, password, profile_image) VALUES (?, ?, ?, ?, ?)",
                                 (user_id, name, email, hashed_pw, icon))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            # UNIQUE制約違反 (user_idまたはemailの重複)  E3: 登録済みデータあり
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
        既存のユーザデータをF1 ユーザ情報で更新する。 
        Args:
            user_id (str): 更新対象のユーザID
            hashed_pw (str, optional): 新しいハッシュ化されたパスワード。Noneの場合は更新しない。
            name (str, optional): 新しい表示名。Noneの場合は更新しない。
            email (str, optional): 新しいメールアドレス。Noneの場合は更新しない。 
            icon (str, optional): 新しいアイコンのファイル名。Noneの場合は更新しない。
        Returns:
            bool: 処理の成否 (True: 成功, False: 失敗 - 例: 該当データなし) 
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
            return False # 更新するフィールドがない場合

        params.append(user_id)
        set_clause = ", ".join(update_fields)

        try:
            self._connect_db() # 更新前にDB接続を再確認
            self.cursor.execute(f"UPDATE users SET {set_clause} WHERE user_id = ?", tuple(params))
            self.conn.commit()
            return self.cursor.rowcount > 0 # 更新された行があるか確認 (E2: 該当データなし) 
        except sqlite3.IntegrityError as e:
            # UNIQUE制約違反 (emailの重複など)
            user_management_logger.warning(f"Integrity error during user update for {user_id}: {e}")
            return False
        except sqlite3.Error as e:
            user_management_logger.error(f"Database error during user update for {user_id}: {e}")
            raise
        finally:
            self._close_db()

    def make_sid(self, user_id):
        """
        M3 SID作成処理に対応 
        ユーザを認証するためのSIDをF2 ユーザ認証情報に作成する。 
        Args:
            user_id (str): SIDを作成するユーザのID
        Returns:
            str or None: 生成されたSID、または失敗した場合None
        """
        user_management_logger.info(f"Attempting to create SID for user_id: {user_id}")
        sid = secrets.token_urlsafe(16) # 16バイトのランダムなURLセーフな文字列を生成 (外部設計書 SID範囲16バイト) 
        try:
            self._connect_db() # SID作成前にDB接続を再確認
            self.cursor.execute("INSERT INTO user_auth (user_id, sid) VALUES (?, ?)", (user_id, sid))
            self.conn.commit()
            return sid
        except sqlite3.IntegrityError as e:
            user_management_logger.warning(f"SID creation failed, user_id {user_id} might already have an SID or constraint violation: {e}")
            return None # 既にSIDが存在する場合など
        except sqlite3.Error as e:
            user_management_logger.error(f"Database error during SID creation for {user_id}: {e}")
            raise
        finally:
            self._close_db()

    def delete_sid(self, sid):
        """
        M4 SID破棄処理に対応 
        入力されたSIDをF2 ユーザ認証情報から破棄する。 
        Args:
            sid (str): 破棄するSID
        Returns:
            bool: 処理の成否 (True: 成功, False: 失敗 - 例: 該当SIDなし) 
        """
        user_management_logger.info(f"Attempting to delete SID: {sid}")
        try:
            self._connect_db() # SID破棄前にDB接続を再確認
            self.cursor.execute("DELETE FROM user_auth WHERE sid = ?", (sid,))
            self.conn.commit()
            return self.cursor.rowcount > 0 # 削除された行があるか確認
        except sqlite3.Error as e:
            user_management_logger.error(f"Database error during SID deletion for {sid}: {e}")
            raise
        finally:
            self._close_db()

    # オブジェクトが破棄されるときにデータベース接続を閉じるためのデストラクタ
    # 各メソッドで接続と切断を行っているので、ここでは不要
    # def __del__(self):
    #     self._close_db()
